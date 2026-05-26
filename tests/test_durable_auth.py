from __future__ import annotations

import asyncio
import importlib
import json
import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock
from urllib.parse import parse_qs, urlparse

from fastapi.testclient import TestClient


MODULES_TO_RESET = [
    "main",
    "settings",
    "crypto",
    "auth_store",
    "cache",
    "config",
]

ENV_KEYS = [
    "SECRET_KEY",
    "AUTH_DB_PATH",
    "ANILIST_CLIENT_ID",
    "ANILIST_CLIENT_SECRET",
    "ANILIST_REDIRECT_URI",
]


class FakeResponse:
    def __init__(self, payload: dict, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload)

    def json(self) -> dict:
        return self._payload


class FakeBinaryResponse:
    def __init__(self, content: bytes, status_code: int = 200) -> None:
        self.content = content
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def make_media(media_id: int, title: str, **overrides) -> dict:
    media = {
        "id": media_id,
        "title": {"english": title, "romaji": title, "native": title},
        "startDate": {"year": 2024, "month": 1, "day": 1},
        "endDate": {"year": 2024, "month": 3, "day": 1},
        "averageScore": 80,
        "meanScore": 80,
        "status": "FINISHED",
        "season": "WINTER",
        "seasonYear": 2024,
        "format": "TV",
        "source": "",
        "popularity": 0,
        "trending": 0,
        "favourites": 0,
        "rankings": [],
        "relations": {"edges": []},
        "nextAiringEpisode": None,
        "coverImage": {"extraLarge": f"https://img.test/{media_id}.jpg"},
        "bannerImage": f"https://img.test/{media_id}-banner.jpg",
        "description": f"{title} description",
        "genres": ["Action"],
        "siteUrl": f"https://anilist.co/anime/{media_id}",
    }
    media.update(overrides)
    return media


class DurableAuthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.original_env = {key: os.environ.get(key) for key in ENV_KEYS}
        self.addCleanup(self._restore_env)

        os.environ["SECRET_KEY"] = "test-secret-key"
        os.environ["AUTH_DB_PATH"] = str(Path(self.tempdir.name) / "auth.db")
        os.environ["ANILIST_CLIENT_ID"] = "test-client-id"
        os.environ["ANILIST_CLIENT_SECRET"] = "test-client-secret"
        os.environ["ANILIST_REDIRECT_URI"] = "http://localhost:7000/oauth/callback"

        self.modules = self.reload_modules()

    def _restore_env(self) -> None:
        for key, value in self.original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def reload_modules(self) -> dict[str, object]:
        for name in MODULES_TO_RESET:
            sys.modules.pop(name, None)

        modules: dict[str, object] = {}
        for name in ["settings", "crypto", "auth_store", "cache", "config", "main"]:
            modules[name] = importlib.import_module(name)
        return modules

    @contextmanager
    def client(self, modules: dict[str, object] | None = None):
        modules = modules or self.modules
        main = modules["main"]
        with mock.patch.object(main.id_mapper, "warmup_indexes", mock.AsyncMock(return_value=False)):
            with TestClient(main.app) as client:
                yield client

    def create_auth_record(self, auth_key: str, *, with_openrouter: bool = False, modules: dict[str, object] | None = None) -> None:
        modules = modules or self.modules
        crypto = modules["crypto"]
        auth_store = modules["auth_store"].auth_store
        encrypted_or = crypto.encrypt("openrouter-secret") if with_openrouter else None
        model = "openai/gpt-4o-mini" if with_openrouter else None
        auth_store.upsert_auth(
            auth_key,
            crypto.encrypt("anilist-access-token"),
            encrypted_openrouter_key=encrypted_or,
            openrouter_model=model,
        )

    def test_auth_store_crud_and_touch_last_used(self) -> None:
        auth_store_module = self.modules["auth_store"]
        store = auth_store_module.auth_store

        with mock.patch.object(auth_store_module.time, "time", return_value=100):
            store.upsert_auth("auth-key", "enc-anilist")
        record = store.get_auth("auth-key")
        self.assertIsNotNone(record)
        self.assertEqual(record["encrypted_anilist_token"], "enc-anilist")
        self.assertEqual(record["created_at"], 100)
        self.assertEqual(record["updated_at"], 100)
        self.assertEqual(record["last_used_at"], 100)

        with mock.patch.object(auth_store_module.time, "time", return_value=150):
            store.update_openrouter(
                "auth-key",
                encrypted_openrouter_key="enc-or",
                openrouter_model="openai/gpt-4o-mini",
            )
        record = store.get_auth("auth-key")
        self.assertEqual(record["encrypted_openrouter_key"], "enc-or")
        self.assertEqual(record["openrouter_model"], "openai/gpt-4o-mini")
        self.assertEqual(record["updated_at"], 150)

        with mock.patch.object(auth_store_module.time, "time", return_value=200):
            record = store.get_auth("auth-key", touch_last_used=True)
        self.assertEqual(record["last_used_at"], 200)
        self.assertEqual(record["updated_at"], 150)

        store.delete_auth("auth-key")
        self.assertIsNone(store.get_auth("auth-key"))

    def test_poster_lab_top_label_prefers_rich_labels_before_rank_fallback(self) -> None:
        main = self.modules["main"]
        now = datetime(2026, 4, 27, 12, 0, tzinfo=timezone.utc)

        returning = make_media(
            1,
            "Returning",
            season="SPRING",
            seasonYear=2026,
            status="RELEASING",
            source="MANGA",
            relations={"edges": [{"relationType": "PREQUEL", "node": {"type": "ANIME"}}]},
        )
        spinoff = make_media(
            2,
            "Spinoff",
            season="SPRING",
            seasonYear=2026,
            status="RELEASING",
            source="MANGA",
            relations={"edges": [{"relationType": "PARENT", "node": {"type": "ANIME"}}]},
        )
        parent_with_side_story = make_media(
            12,
            "Parent Show",
            source="MANGA",
            relations={"edges": [{"relationType": "SIDE_STORY", "node": {"type": "ANIME"}}]},
        )
        new_season = make_media(3, "New Season", season="SPRING", seasonYear=2026, status="NOT_YET_RELEASED")
        movie_premiere = make_media(
            4,
            "Movie Premiere",
            format="MOVIE",
            source="MANGA",
            startDate={"year": 2026, "month": 5, "day": 10},
        )
        manga = make_media(5, "Manga", source="MANGA", startDate={"year": 2026, "month": 4, "day": 20})
        ln = make_media(6, "Light Novel", source="LIGHT_NOVEL")
        game = make_media(7, "Game", source="VIDEO_GAME")
        recently_adapted = make_media(8, "Novel", source="NOVEL", startDate={"year": 2026, "month": 3, "day": 15})
        original = make_media(9, "Original", source="ORIGINAL")
        airs_this_week = make_media(10, "Airs This Week", status="RELEASING", nextAiringEpisode={"episode": 4, "timeUntilAiring": 7200})
        no_label = make_media(11, "No Label")

        self.assertEqual(main._poster_lab_top_label(returning, [returning], now=now), "Returning Series")
        self.assertEqual(main._poster_lab_top_label(spinoff, [spinoff], now=now), "Spin-off")
        self.assertEqual(main._poster_lab_top_label(new_season, [new_season], now=now), "New Season")
        self.assertEqual(main._poster_lab_top_label(movie_premiere, [movie_premiere], now=now), "Movie Premiere")
        self.assertEqual(main._poster_lab_top_label(manga, [manga], now=now), "Manga Adaptation")
        self.assertEqual(main._poster_lab_top_label(ln, [ln], now=now), "LN Adaptation")
        self.assertEqual(main._poster_lab_top_label(game, [game], now=now), "Game Adaptation")
        self.assertEqual(main._poster_lab_top_label(recently_adapted, [recently_adapted], now=now), "Recently Adapted")
        self.assertEqual(main._poster_lab_top_label(original, [original], now=now), "Original Anime")
        self.assertEqual(main._poster_lab_top_label(airs_this_week, [airs_this_week], now=now), "Airs This Week")
        self.assertEqual(main._poster_lab_top_label(parent_with_side_story, [parent_with_side_story], now=now), "Manga Adaptation")
        self.assertIsNone(main._poster_lab_top_label(no_label, [no_label], now=now))

    def test_poster_lab_top_labels_handle_page_relative_trending_and_rank_fallback(self) -> None:
        main = self.modules["main"]
        now = datetime(2026, 4, 27, 12, 0, tzinfo=timezone.utc)

        trending_page = [
            make_media(media_id, f"Trending {media_id}", trending=500 - media_id)
            for media_id in range(20, 31)
        ]
        trending_target = make_media(
            99,
            "Trending Winner",
            trending=999,
            rankings=[{"rank": 7, "type": "POPULAR", "allTime": True}],
        )
        rank_fallback = make_media(
            199,
            "Rank Fallback",
            trending=1,
            rankings=[{"rank": 33, "type": "RATED", "allTime": True}],
        )
        page_media = [trending_target, *trending_page, rank_fallback]

        labels = main._poster_lab_top_labels(page_media, now=now)

        self.assertEqual(labels[99], "#7 Most Popular")
        self.assertEqual(labels[199], "#33 Highest Rated")

    def test_poster_lab_effect_profile_boosts_clean_and_rating_only(self) -> None:
        main = self.modules["main"]

        self.assertEqual(
            main._poster_lab_effect_profile("clean"),
            {
                "blur_ratio": 0.34,
                "blur_alpha": 236,
                "blur_min_radius": 10,
                "blur_width_divisor": 46,
                "shadow_ratio": 0.24,
                "shadow_alpha": 132,
            },
        )
        self.assertEqual(
            main._poster_lab_effect_profile("rating"),
            {
                "blur_ratio": 0.34,
                "blur_alpha": 236,
                "blur_min_radius": 10,
                "blur_width_divisor": 46,
                "shadow_ratio": 0.24,
                "shadow_alpha": 132,
            },
        )
        self.assertEqual(
            main._poster_lab_effect_profile("rank"),
            {
                "blur_ratio": 0.26,
                "blur_alpha": 220,
                "blur_min_radius": 8,
                "blur_width_divisor": 58,
                "shadow_ratio": 0.20,
                "shadow_alpha": 105,
            },
        )

    def test_poster_lab_render_returns_png_for_clean_and_rating(self) -> None:
        import io

        from PIL import Image

        main = self.modules["main"]
        image_bytes = io.BytesIO()
        Image.new("RGB", (240, 360), (42, 58, 96)).save(image_bytes, format="PNG")
        upstream = FakeBinaryResponse(image_bytes.getvalue())
        source_url = "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx123.jpg"

        with self.client() as client, mock.patch.object(
            main,
            "_request_with_general_client",
            mock.AsyncMock(return_value=upstream),
        ):
            for style in ("clean", "rating"):
                with self.subTest(style=style):
                    response = client.get(
                        "/poster-lab/render.png",
                        params={
                            "src": source_url,
                            "top": "#7 Highest Rated",
                            "bottom": "Action|8.5",
                            "style": style,
                            "v": main.POSTER_LAB_VERSION,
                        },
                    )

                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.headers["content-type"], "image/png")
                    self.assertGreater(len(response.content), 0)

    def test_map_catalog_media_canonicalizes_multiple_replacements_to_one_s1_tile(self) -> None:
        main = self.modules["main"]
        sequel_one = make_media(701, "Canon Saga Season 2")
        sequel_two = make_media(702, "Canon Saga Season 3")
        season_one = make_media(
            601,
            "Canon Saga",
            averageScore=91,
            coverImage={"extraLarge": "https://img.test/canon-s1.jpg", "color": "#224466"},
            bannerImage="https://img.test/canon-s1-banner.jpg",
        )

        async def fake_batch_map_ids(media_list: list[dict]) -> tuple[dict[int, str], dict[int, tuple[int, str]]]:
            mapping = {media["id"]: f"tt{media['id']:07d}" for media in media_list}
            replacements = {media["id"]: (601, "tt0000601") for media in media_list}
            return mapping, replacements

        with mock.patch.object(main, "batch_map_ids", mock.AsyncMock(side_effect=fake_batch_map_ids)), \
            mock.patch.object(main.anilist, "get_media_by_ids", mock.AsyncMock(return_value=[season_one])):
            result = asyncio.run(main._map_catalog_media([sequel_one, sequel_two]))

        self.assertEqual([media["id"] for media in result["media"]], [601])
        self.assertEqual(result["media"][0]["title"]["english"], "Canon Saga")
        self.assertEqual(result["media"][0]["bannerImage"], "https://img.test/canon-s1-banner.jpg")
        self.assertEqual(result["id_mapping"], {601: "tt0000601"})
        self.assertEqual(result["s1_fetch_failures"], 0)

    def test_map_catalog_media_falls_back_to_original_when_s1_hydration_fails(self) -> None:
        main = self.modules["main"]
        sequel = make_media(701, "Canon Saga Season 2")

        async def fake_batch_map_ids(media_list: list[dict]) -> tuple[dict[int, str], dict[int, tuple[int, str]]]:
            mapping = {media["id"]: f"tt{media['id']:07d}" for media in media_list}
            replacements = {media["id"]: (601, "tt0000601") for media in media_list}
            return mapping, replacements

        with mock.patch.object(main, "batch_map_ids", mock.AsyncMock(side_effect=fake_batch_map_ids)), \
            mock.patch.object(main.anilist, "get_media_by_ids", mock.AsyncMock(side_effect=RuntimeError("boom"))):
            result = asyncio.run(main._map_catalog_media([sequel]))

        self.assertEqual([media["id"] for media in result["media"]], [701])
        self.assertEqual(result["media"][0]["title"]["english"], "Canon Saga Season 2")
        self.assertEqual(result["id_mapping"], {701: "tt0000701"})
        self.assertEqual(result["s1_fetch_failures"], 1)

    def test_map_catalog_media_retries_smaller_s1_batches_after_batch_failure(self) -> None:
        main = self.modules["main"]
        sequels = [
            make_media(701, "Canon Saga Season 2"),
            make_media(702, "Canon Saga Season 3"),
            make_media(703, "Canon Saga Season 4"),
            make_media(704, "Canon Saga Season 5"),
        ]
        season_one_media = {
            601: make_media(601, "Canon Saga"),
            602: make_media(602, "Mystery School"),
            603: make_media(603, "Space Days"),
            604: make_media(604, "Action Club"),
        }

        async def fake_batch_map_ids(media_list: list[dict]) -> tuple[dict[int, str], dict[int, tuple[int, str]]]:
            mapping = {media["id"]: f"tt{media['id']:07d}" for media in media_list}
            replacements = {
                701: (601, "tt0000601"),
                702: (602, "tt0000602"),
                703: (603, "tt0000603"),
                704: (604, "tt0000604"),
            }
            return mapping, replacements

        async def fake_get_media_by_ids(anilist_ids: list[int], media_fields=None) -> list[dict]:
            if len(anilist_ids) > 2:
                raise RuntimeError("query too large")
            return [season_one_media[anilist_id] for anilist_id in anilist_ids]

        with mock.patch.object(main, "batch_map_ids", mock.AsyncMock(side_effect=fake_batch_map_ids)), \
            mock.patch.object(main.anilist, "get_media_by_ids", mock.AsyncMock(side_effect=fake_get_media_by_ids)):
            result = asyncio.run(main._map_catalog_media(sequels))

        self.assertEqual([media["id"] for media in result["media"]], [601, 602, 603, 604])
        self.assertEqual(
            result["id_mapping"],
            {
                601: "tt0000601",
                602: "tt0000602",
                603: "tt0000603",
                604: "tt0000604",
            },
        )
        self.assertEqual(result["s1_fetch_failures"], 0)

    def test_catalog_routes_return_same_canonical_tile_across_source_types(self) -> None:
        auth_key = "canonical-routes"
        self.create_auth_record(auth_key)
        main = self.modules["main"]
        config = self.modules["config"]
        config_token = config.encode_config(
            {
                "catalogs": [
                    {"id": "anilist-popular-season", "name": "Popular This Season", "type": "preset"},
                    {"id": "custom-canon", "name": "Canon Custom", "type": "custom", "filters": {}},
                    {
                        "id": "anilist-watching-current",
                        "name": "Currently Watching",
                        "type": "watching",
                        "listStatus": "CURRENT",
                    },
                ]
            }
        )
        segment = f"{config_token}~{auth_key}"
        preset_media = make_media(701, "Canon Saga Season 2")
        custom_media = make_media(702, "Canon Saga Season 3")
        watching_media = make_media(703, "Canon Saga Season 4")
        season_one = make_media(
            601,
            "Canon Saga",
            averageScore=92,
            coverImage={"extraLarge": "https://img.test/canon-s1.jpg", "color": "#335577"},
            bannerImage="https://img.test/canon-s1-banner.jpg",
            description="Canonical season one description",
        )

        async def fake_batch_map_ids(media_list: list[dict]) -> tuple[dict[int, str], dict[int, tuple[int, str]]]:
            mapping = {media["id"]: f"tt{media['id']:07d}" for media in media_list}
            replacements = {
                media["id"]: (601, "tt0000601")
                for media in media_list
                if media["id"] in {701, 702, 703}
            }
            return mapping, replacements

        with self.client() as client, \
            mock.patch.dict(
                main.PRESET_HANDLERS,
                {"anilist-popular-season": mock.AsyncMock(return_value=[preset_media])},
                clear=False,
            ), \
            mock.patch.object(main.anilist, "get_custom", mock.AsyncMock(return_value=[custom_media])), \
            mock.patch.object(
                main.anilist,
                "get_viewer",
                mock.AsyncMock(return_value={"id": 44, "name": "Jordan", "avatar": "https://img.test/avatar.jpg"}),
            ), \
            mock.patch.object(main.anilist, "get_watching_list", mock.AsyncMock(return_value=[watching_media])), \
            mock.patch.object(main, "batch_map_ids", mock.AsyncMock(side_effect=fake_batch_map_ids)), \
            mock.patch.object(main.anilist, "get_media_by_ids", mock.AsyncMock(return_value=[season_one])):
            preset_response = client.get(f"/{segment}/catalog/series/anilist-popular-season.json")
            custom_response = client.get(f"/{segment}/catalog/series/custom-canon.json")
            watching_response = client.get(f"/{segment}/catalog/series/anilist-watching-current.json")

        for response in (preset_response, custom_response, watching_response):
            self.assertEqual(response.status_code, 200)

        preset_meta = preset_response.json()["metas"][0]
        custom_meta = custom_response.json()["metas"][0]
        watching_meta = watching_response.json()["metas"][0]

        self.assertEqual(preset_meta["id"], "tt0000601")
        self.assertEqual(preset_meta["name"], "Canon Saga")
        self.assertEqual(preset_meta["poster"], "https://img.test/canon-s1.jpg")
        self.assertEqual(preset_meta["background"], "https://img.test/canon-s1-banner.jpg")
        self.assertEqual(custom_meta["id"], preset_meta["id"])
        self.assertEqual(custom_meta["name"], preset_meta["name"])
        self.assertEqual(custom_meta["poster"], preset_meta["poster"])
        self.assertEqual(custom_meta["background"], preset_meta["background"])
        self.assertEqual(watching_meta["id"], preset_meta["id"])
        self.assertEqual(watching_meta["name"], preset_meta["name"])
        self.assertEqual(watching_meta["poster"], preset_meta["poster"])
        self.assertEqual(watching_meta["background"], preset_meta["background"])

    def test_poster_lab_catalogs_share_canonical_banner_inputs_after_s1_normalization(self) -> None:
        auth_key = "canonical-poster-lab"
        self.create_auth_record(auth_key)
        main = self.modules["main"]
        config = self.modules["config"]
        config_token = config.encode_config(
            {
                "posterStyle": "clean",
                "catalogs": [
                    {"id": "anilist-popular-season", "name": "Popular This Season", "type": "preset"},
                    {"id": "custom-canon", "name": "Canon Custom", "type": "custom", "filters": {}},
                ],
            }
        )
        segment = f"{config_token}~{auth_key}"
        preset_media = make_media(701, "Canon Saga Season 2")
        custom_media = make_media(702, "Canon Saga Season 3")
        season_one = make_media(
            601,
            "Canon Saga",
            rankings=[{"rank": 17, "type": "POPULAR", "allTime": True}],
            averageScore=92,
            coverImage={"extraLarge": "https://img.test/canon-s1.jpg", "color": "#335577"},
            bannerImage="https://img.test/canon-s1-banner.jpg",
        )

        async def fake_batch_map_ids(media_list: list[dict]) -> tuple[dict[int, str], dict[int, tuple[int, str]]]:
            mapping = {media["id"]: f"tt{media['id']:07d}" for media in media_list}
            replacements = {
                media["id"]: (601, "tt0000601")
                for media in media_list
                if media["id"] in {701, 702}
            }
            return mapping, replacements

        with self.client() as client, \
            mock.patch.dict(
                main.PRESET_HANDLERS,
                {"anilist-popular-season": mock.AsyncMock(return_value=[preset_media])},
                clear=False,
            ), \
            mock.patch.object(main.anilist, "get_custom", mock.AsyncMock(return_value=[custom_media])), \
            mock.patch.object(main, "batch_map_ids", mock.AsyncMock(side_effect=fake_batch_map_ids)), \
            mock.patch.object(main.anilist, "get_media_by_ids", mock.AsyncMock(return_value=[season_one])):
            preset_response = client.get(f"/{segment}/poster-lab/catalog/series/anilist-popular-season.json")
            custom_response = client.get(f"/{segment}/poster-lab/catalog/series/custom-canon.json")

        self.assertEqual(preset_response.status_code, 200)
        self.assertEqual(custom_response.status_code, 200)

        preset_poster = preset_response.json()["metas"][0]["poster"]
        custom_poster = custom_response.json()["metas"][0]["poster"]
        self.assertEqual(preset_poster, custom_poster)

        poster_params = parse_qs(urlparse(preset_poster).query)
        self.assertEqual(poster_params["src"][0], "https://img.test/canon-s1.jpg")
        self.assertEqual(poster_params["top"][0], "#17 Most Popular")
        self.assertEqual(poster_params["style"][0], "clean")

    def test_get_airing_week_query_uses_canonical_catalog_fields(self) -> None:
        anilist_module = self.modules["main"].anilist

        with mock.patch.object(
            anilist_module,
            "_gql",
            mock.AsyncMock(return_value={"Page": {"airingSchedules": []}}),
        ) as gql_mock:
            result = asyncio.run(anilist_module.get_airing_week())

        self.assertEqual(result, [])
        query = gql_mock.await_args.args[0]
        self.assertIn("bannerImage", query)
        self.assertIn("rankings { rank type allTime context }", query)
        self.assertIn("relations { edges { relationType(version: 2) node { type } } }", query)
        self.assertIn("nextAiringEpisode { episode timeUntilAiring }", query)
        self.assertIn("isAdult", query)

    def test_catalog_filter_normalization_strips_invalid_values_and_keeps_one_season(self) -> None:
        anilist_module = self.modules["main"].anilist

        normalized = anilist_module.normalize_catalog_filters(
            {
                "sort": "TRENDING_DESC",
                "genres": ["Action", "", "Action"],
                "formats": ["", "TV", "TV", "BAD_FORMAT"],
                "statuses": ["", "RELEASING", "BAD_STATUS"],
                "seasons": ["CURRENT", "SUMMER", "BAD_SEASON"],
                "years": ["2024", "2025", "bad"],
                "daterange": "this-year",
            }
        )

        self.assertEqual(
            normalized,
            {
                "sort": "TRENDING_DESC",
                "genres": ["Action"],
                "formats": ["TV"],
                "statuses": ["RELEASING"],
                "seasons": ["SUMMER"],
                "years": ["2025"],
            },
        )

    def test_current_season_filter_overrides_explicit_year_and_last_year(self) -> None:
        anilist_module = self.modules["main"].anilist

        with mock.patch.object(anilist_module, "_season_now", return_value=("SPRING", 2026)), \
            mock.patch.object(
                anilist_module,
                "_gql",
                mock.AsyncMock(return_value={"Page": {"media": []}}),
            ) as gql_mock:
            result = asyncio.run(
                anilist_module.get_custom(
                    {"seasons": ["CURRENT"], "years": ["2024"], "daterange": "last-year"},
                    page=1,
                    per_page=10,
                )
            )

        self.assertEqual(result, [])
        variables = gql_mock.await_args.args[1]
        self.assertEqual(variables["season"], "SPRING")
        self.assertEqual(variables["year"], 2026)
        self.assertNotIn("sdGt", variables)
        self.assertNotIn("sdLt", variables)

    def test_explicit_year_drops_year_date_range_and_blank_enum_values(self) -> None:
        anilist_module = self.modules["main"].anilist

        with mock.patch.object(
            anilist_module,
            "_gql",
            mock.AsyncMock(return_value={"Page": {"media": []}}),
        ) as gql_mock:
            result = asyncio.run(
                anilist_module.get_custom(
                    {
                        "formats": ["", "TV", "BAD_FORMAT"],
                        "statuses": ["", "RELEASING"],
                        "years": ["2024"],
                        "daterange": "this-year",
                    },
                    page=1,
                    per_page=10,
                )
            )

        self.assertEqual(result, [])
        variables = gql_mock.await_args.args[1]
        self.assertEqual(variables["formats"], ["TV"])
        self.assertEqual(variables["statuses"], ["RELEASING"])
        self.assertEqual(variables["year"], 2024)
        self.assertNotIn("sdGt", variables)
        self.assertNotIn("sdLt", variables)

    def test_short_date_range_custom_catalog_uses_media_trends_and_filters_locally(self) -> None:
        anilist_module = self.modules["main"].anilist
        high_trending = make_media(
            101,
            "High Trending",
            genres=["Action", "Adventure"],
            format="TV",
            status="RELEASING",
            season="SPRING",
            seasonYear=2026,
            averageScore=82,
            popularity=100,
            trending=50,
            isAdult=False,
        )
        popular_but_less_trending = make_media(
            102,
            "Popular But Less Trending",
            genres=["Action", "Adventure"],
            format="TV",
            status="RELEASING",
            season="SPRING",
            seasonYear=2026,
            averageScore=90,
            popularity=999,
            trending=5,
            isAdult=False,
        )
        adult_match = make_media(
            103,
            "Adult Match",
            genres=["Action", "Adventure"],
            format="TV",
            status="RELEASING",
            season="SPRING",
            seasonYear=2026,
            averageScore=99,
            popularity=2000,
            trending=999,
            isAdult=True,
        )
        wrong_genre = make_media(
            104,
            "Wrong Genre",
            genres=["Action"],
            format="TV",
            status="RELEASING",
            season="SPRING",
            seasonYear=2026,
            averageScore=95,
            popularity=1500,
            trending=100,
            isAdult=False,
        )
        wrong_status = make_media(
            105,
            "Wrong Status",
            genres=["Action", "Adventure"],
            format="TV",
            status="FINISHED",
            season="SPRING",
            seasonYear=2026,
            averageScore=95,
            popularity=1500,
            trending=100,
            isAdult=False,
        )
        low_score = make_media(
            106,
            "Low Score",
            genres=["Action", "Adventure"],
            format="TV",
            status="RELEASING",
            season="SPRING",
            seasonYear=2026,
            averageScore=40,
            popularity=1500,
            trending=100,
            isAdult=False,
        )

        media_payload = {
            "Page": {
                "media": [
                    adult_match,
                    high_trending,
                    wrong_genre,
                    popular_but_less_trending,
                    wrong_status,
                    low_score,
                    high_trending,
                ],
            }
        }
        trend_payload = {
            "Page": {
                "pageInfo": {"hasNextPage": False},
                "mediaTrends": [
                    {"mediaId": 101, "date": 1778511600, "trending": 100},
                    {"mediaId": 101, "date": 1778598000, "trending": 40},
                    {"mediaId": 102, "date": 1778511600, "trending": 200},
                    {"mediaId": 103, "date": 1778511600, "trending": 999},
                    {"mediaId": 104, "date": 1778511600, "trending": 500},
                    {"mediaId": 105, "date": 1778511600, "trending": 500},
                    {"mediaId": 106, "date": 1778511600, "trending": 500},
                ],
            }
        }
        filters = {
            "daterange": "this-month",
            "sort": "TRENDING_DESC",
            "genres": ["Action", "Adventure"],
            "formats": ["TV"],
            "statuses": ["RELEASING"],
            "seasons": ["SPRING"],
            "years": ["2026"],
            "minScore": 70,
        }

        async def fake_gql(query, variables, token=None):
            if "mediaTrends" in query:
                return trend_payload
            return media_payload

        with mock.patch.object(anilist_module, "_gql", mock.AsyncMock(side_effect=fake_gql)) as gql_mock:
            result = asyncio.run(anilist_module.get_custom(filters, page=1, per_page=50))

        self.assertEqual([media["id"] for media in result], [102, 101])
        queries = [call.args[0] for call in gql_mock.await_args_list]
        self.assertTrue(any("mediaTrends" in query for query in queries))
        self.assertFalse(any("airingSchedules" in query for query in queries))
        self.assertFalse(any("startDate_greater" in query for query in queries))
        self.assertEqual(result[0]["trendWindowScore"], 200)
        self.assertEqual(result[1]["trendWindowScore"], 140)

    def test_short_date_range_sort_is_independent_of_trend_filter(self) -> None:
        anilist_module = self.modules["main"].anilist
        high_score = make_media(301, "High Score", averageScore=95, popularity=10, trending=5)
        high_popularity = make_media(302, "High Popularity", averageScore=70, popularity=999, trending=5)
        no_trend = make_media(303, "No Trend", averageScore=100, popularity=1000, trending=0)
        media_payload = {"Page": {"media": [high_score, high_popularity, no_trend]}}
        trend_payload = {
            "Page": {
                "pageInfo": {"hasNextPage": False},
                "mediaTrends": [
                    {"mediaId": 301, "date": 1778511600, "trending": 10},
                    {"mediaId": 302, "date": 1778511600, "trending": 20},
                ],
            }
        }

        async def fake_gql(query, variables, token=None):
            if "mediaTrends" in query:
                return trend_payload
            return media_payload

        with mock.patch.object(anilist_module, "_gql", mock.AsyncMock(side_effect=fake_gql)):
            popular = asyncio.run(anilist_module.get_custom({"daterange": "this-week", "sort": "POPULARITY_DESC"}, page=1, per_page=50))
            self.modules["cache"].cache.clear()
            scored = asyncio.run(anilist_module.get_custom({"daterange": "this-week", "sort": "SCORE_DESC"}, page=1, per_page=50))
            self.modules["cache"].cache.clear()
            trending = asyncio.run(anilist_module.get_custom({"daterange": "this-week", "sort": "TRENDING_DESC"}, page=1, per_page=50))

        self.assertEqual([media["id"] for media in popular], [302, 301])
        self.assertEqual([media["id"] for media in scored], [301, 302])
        self.assertEqual([media["id"] for media in trending], [302, 301])
        self.assertNotIn(303, [media["id"] for media in trending])

    def test_catalog_client_filter_sort_modes_are_applied_consistently(self) -> None:
        main = self.modules["main"]
        older = make_media(
            201,
            "Older",
            popularity=100,
            trending=5,
            averageScore=60,
            favourites=10,
            seasonYear=2024,
            startDate={"year": 2024, "month": 1, "day": 1},
        )
        newer = make_media(
            202,
            "Newer",
            popularity=20,
            trending=50,
            averageScore=90,
            favourites=5,
            seasonYear=2026,
            startDate={"year": 2026, "month": 5, "day": 10},
        )
        favourite = make_media(
            203,
            "Favourite",
            popularity=80,
            trending=10,
            averageScore=70,
            favourites=100,
            seasonYear=2025,
            startDate={"year": 2025, "month": 8, "day": 1},
        )
        media = [older, newer, favourite]

        self.assertEqual(
            [m["id"] for m in main._apply_client_filters_to_media(media, {"sort": "TRENDING_DESC"})],
            [202, 203, 201],
        )
        self.assertEqual(
            [m["id"] for m in main._apply_client_filters_to_media(media, {"sort": "POPULARITY_DESC"})],
            [201, 203, 202],
        )
        self.assertEqual(
            [m["id"] for m in main._apply_client_filters_to_media(media, {"sort": "SCORE_DESC"})],
            [202, 203, 201],
        )
        self.assertEqual(
            [m["id"] for m in main._apply_client_filters_to_media(media, {"sort": "START_DATE_DESC"})],
            [202, 203, 201],
        )
        self.assertEqual(
            [m["id"] for m in main._apply_client_filters_to_media(media, {"sort": "FAVOURITES_DESC"})],
            [203, 201, 202],
        )

    def test_source_backed_short_date_filter_uses_media_trends_for_source_ids(self) -> None:
        main = self.modules["main"]
        source_media = [
            make_media(401, "Trend Source", popularity=10, trending=1),
            make_media(402, "Quiet Source", popularity=999, trending=0),
        ]

        with mock.patch.object(
            main.anilist,
            "get_media_trends_for_ids",
            mock.AsyncMock(return_value={401: {"score": 50, "peak": 50, "days": 1, "popularity": 10, "inProgress": 3}}),
        ) as trends_mock:
            result = asyncio.run(
                main._apply_client_filters_to_media_async(
                    source_media,
                    {"daterange": "this-week", "sort": "POPULARITY_DESC"},
                )
            )

        self.assertEqual([media["id"] for media in result], [401])
        trends_mock.assert_awaited_once()

    def test_source_backed_client_filters_use_shared_normalization(self) -> None:
        main = self.modules["main"]
        source_media = [
            make_media(
                601,
                "Summer Match",
                format="TV",
                status="RELEASING",
                season="SUMMER",
                seasonYear=2026,
                startDate={"year": 2020, "month": 1, "day": 1},
            ),
            make_media(
                602,
                "Spring Nonmatch",
                format="TV",
                status="RELEASING",
                season="SPRING",
                seasonYear=2026,
                startDate={"year": 2026, "month": 5, "day": 1},
            ),
        ]

        result = main._apply_client_filters_to_media(
            source_media,
            {
                "formats": ["", "TV", "BAD_FORMAT"],
                "statuses": ["", "RELEASING"],
                "seasons": ["CURRENT", "SUMMER"],
                "years": ["2026"],
                "daterange": "this-year",
                "sort": "POPULARITY_DESC",
            },
        )

        self.assertEqual([media["id"] for media in result], [601])

    def test_media_trend_failure_falls_back_to_candidate_results(self) -> None:
        anilist_module = self.modules["main"].anilist
        candidate = make_media(501, "Fallback Candidate", popularity=50, trending=5)

        async def fake_gql(query, variables, token=None):
            if "mediaTrends" in query:
                raise RuntimeError("rate limited")
            return {"Page": {"media": [candidate]}}

        with mock.patch.object(anilist_module, "_gql", mock.AsyncMock(side_effect=fake_gql)):
            result = asyncio.run(anilist_module.get_custom({"daterange": "this-week", "sort": "TRENDING_DESC"}))

        self.assertEqual([media["id"] for media in result], [501])

    def test_year_date_range_custom_catalog_stays_start_date_based(self) -> None:
        anilist_module = self.modules["main"].anilist

        with mock.patch.object(
            anilist_module,
            "_gql",
            mock.AsyncMock(return_value={"Page": {"media": []}}),
        ) as gql_mock:
            result = asyncio.run(anilist_module.get_custom({"daterange": "this-year", "sort": "TRENDING_DESC"}))

        self.assertEqual(result, [])
        query = gql_mock.await_args.args[0]
        self.assertIn("media(", query)
        self.assertIn("startDate_greater", query)
        self.assertNotIn("airingSchedules", query)
        self.assertNotIn("mediaTrends", query)

    def test_get_media_by_ids_query_uses_canonical_catalog_fields(self) -> None:
        anilist_module = self.modules["main"].anilist

        with mock.patch.object(
            anilist_module,
            "_gql",
            mock.AsyncMock(return_value={"a0": {"id": 601}, "a1": {"id": 602}}),
        ) as gql_mock:
            result = asyncio.run(anilist_module.get_media_by_ids([601, 602]))

        self.assertEqual([media["id"] for media in result], [601, 602])
        query = gql_mock.await_args.args[0]
        self.assertIn("a0: Media(id: 601, type: ANIME)", query)
        self.assertIn("bannerImage", query)
        self.assertIn("rankings { rank type allTime context }", query)
        self.assertIn("relations { edges { relationType(version: 2) node { type } } }", query)
        self.assertIn("nextAiringEpisode { episode timeUntilAiring }", query)
        self.assertIn("isAdult", query)

    def test_catalog_cache_key_is_scoped_and_versioned(self) -> None:
        main = self.modules["main"]

        preset_key = main._poster_lab_cache_key(
            "anilist-popular-season",
            1,
            cache_scope='{"id":"anilist-popular-season","name":"Popular This Season","type":"preset"}',
        )
        renamed_key = main._poster_lab_cache_key(
            "anilist-popular-season",
            1,
            cache_scope='{"id":"anilist-popular-season","name":"Renamed Row","type":"preset"}',
        )
        poster_lab_key = main._poster_lab_cache_key(
            "anilist-popular-season",
            1,
            cache_scope='{"id":"anilist-popular-season","name":"Popular This Season","type":"preset"}',
            poster_variant=main.POSTER_LAB_VARIANT,
            poster_base_url="http://testserver",
            poster_style="clean",
        )

        self.assertIn("cache:v3", preset_key)
        self.assertNotEqual(preset_key, renamed_key)
        self.assertIn("variant:poster-lab:clean", poster_lab_key)
        self.assertIn("cache:v3", poster_lab_key)

    def test_oauth_callback_persists_auth_and_survives_restart(self) -> None:
        main = self.modules["main"]
        auth_store = self.modules["auth_store"].auth_store

        with self.client() as client, \
            mock.patch.object(
                main,
                "_request_with_general_client",
                mock.AsyncMock(return_value=FakeResponse({"access_token": "oauth-token"})),
            ):
            response = client.get(
                "/oauth/callback?code=test-code&state=csrf-state",
                cookies={"oauth_state": "csrf-state"},
                follow_redirects=False,
            )

        self.assertEqual(response.status_code, 307)
        location = response.headers["location"]
        self.assertIn("#s=", location)
        auth_key = location.split("#s=", 1)[1]
        self.assertIsNotNone(auth_store.get_auth(auth_key))

        self.modules["cache"].cache.clear()
        reloaded = self.reload_modules()

        with self.client(reloaded) as client, \
            mock.patch.object(
                reloaded["main"].anilist,
                "get_viewer",
                mock.AsyncMock(return_value={"id": 7, "name": "Jordan", "avatar": "https://img.test/avatar.jpg"}),
            ):
            response = client.post("/api/me", json={"session": auth_key})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Jordan")
        self.assertFalse(response.json()["has_or_key"])

    def test_save_openrouter_key_and_preview_ai_survive_cache_clear(self) -> None:
        auth_key = "durable-ai"
        self.create_auth_record(auth_key)

        main = self.modules["main"]
        with self.client() as client, \
            mock.patch.object(main, "_validate_openrouter_key", mock.AsyncMock(return_value=(True, None))), \
            mock.patch.object(
                main.anilist,
                "get_viewer",
                mock.AsyncMock(return_value={"id": 9, "name": "Jordan", "avatar": "https://img.test/avatar.jpg"}),
            ), \
            mock.patch.object(
                main.anilist,
                "get_ai_recommendations",
                mock.AsyncMock(return_value=[make_media(301, "AI Pick")]),
            ) as get_ai_recommendations:
            save_response = client.post(
                "/api/save-openrouter-key",
                json={
                    "session": auth_key,
                    "key": "or-key",
                    "model": "openai/gpt-4o-mini",
                },
            )
            self.assertEqual(save_response.status_code, 200)

            record = self.modules["auth_store"].auth_store.get_auth(auth_key)
            self.assertIsNotNone(record["encrypted_openrouter_key"])
            self.assertEqual(record["openrouter_model"], "openai/gpt-4o-mini")

            first_preview = client.post("/api/preview-ai", json={"session": auth_key})
            self.assertEqual(first_preview.status_code, 200)
            self.assertEqual(get_ai_recommendations.await_count, 1)

            self.modules["cache"].cache.clear()

            me_response = client.post("/api/me", json={"session": auth_key})
            self.assertEqual(me_response.status_code, 200)
            self.assertTrue(me_response.json()["has_or_key"])
            self.assertEqual(me_response.json()["or_model"], "openai/gpt-4o-mini")

            second_preview = client.post("/api/preview-ai", json={"session": auth_key})
            self.assertEqual(second_preview.status_code, 200)
            self.assertEqual(get_ai_recommendations.await_count, 2)

    def test_smart_ai_cache_key_separates_seed_configs(self) -> None:
        main = self.modules["main"]
        frieren = {
            "type": "ai",
            "aiMode": "title_seed",
            "seedTitle": "Frieren",
            "smartOptions": {"formats": ["TV"], "minScore": 70, "popularityBias": "balanced"},
        }
        dandadan = {
            "type": "ai",
            "aiMode": "title_seed",
            "seedTitle": "Dandadan",
            "smartOptions": {"formats": ["TV"], "minScore": 70, "popularityBias": "balanced"},
        }

        self.assertNotEqual(
            main._ai_catalog_cache_key("session", "model/a", frieren),
            main._ai_catalog_cache_key("session", "model/a", dandadan),
        )
        self.assertEqual(
            main._ai_catalog_cache_key("session", "model/a", {"type": "ai"}),
            main._ai_catalog_cache_key("session", "model/a", {"type": "ai", "name": "Renamed Legacy"}),
        )

    def test_smart_ai_prompt_generation_for_modes(self) -> None:
        anilist = self.modules["main"].anilist
        completed = [
            {"media": make_media(401, "Frieren"), "user_score": 10},
            {"media": make_media(402, "Ping Pong"), "user_score": 9},
        ]
        watching = [{"media": make_media(403, "Dandadan"), "user_score": 0}]

        _system, title_prompt, _seeds, _completed = anilist._build_ai_recommendation_prompts(
            completed,
            watching,
            completed + watching,
            {"aiMode": "title_seed", "seedTitle": "Frieren", "smartOptions": {"popularityBias": "balanced"}},
        )
        self.assertIn("Frieren", title_prompt)
        self.assertIn("selected seed", title_prompt)

        _system, top_prompt, _seeds, _completed = anilist._build_ai_recommendation_prompts(
            completed,
            watching,
            completed + watching,
            {"aiMode": "top_rated", "smartOptions": {"minScore": 70}},
        )
        self.assertIn("highest-rated", top_prompt)
        self.assertIn("10/10", top_prompt)

        _system, hidden_prompt, _seeds, _completed = anilist._build_ai_recommendation_prompts(
            completed,
            watching,
            completed + watching,
            {"aiMode": "hidden_completed", "smartOptions": {"popularityBias": "hidden"}},
        )
        self.assertIn("hidden gems", hidden_prompt)
        self.assertIn("lower-popularity", hidden_prompt)

    def test_preview_ai_rejects_missing_openrouter_for_smart_row(self) -> None:
        auth_key = "smart-no-or"
        self.create_auth_record(auth_key)

        with self.client() as client:
            response = client.post(
                "/api/preview-ai",
                json={
                    "session": auth_key,
                    "catalog": {
                        "id": "ai-smart",
                        "name": "More like Frieren",
                        "type": "ai",
                        "aiMode": "title_seed",
                        "seedTitle": "Frieren",
                    },
                },
            )

        self.assertEqual(response.status_code, 400)
        self.assertIn("OpenRouter", response.json()["detail"])

    def test_smart_ai_preview_and_catalog_share_cache_path(self) -> None:
        auth_key = "smart-cache"
        self.create_auth_record(auth_key, with_openrouter=True)
        main = self.modules["main"]
        config = self.modules["config"]
        catalog = {
            "id": "ai-frieren",
            "name": "More like Frieren",
            "type": "ai",
            "aiMode": "title_seed",
            "seedTitle": "Frieren",
            "smartOptions": {"formats": ["TV"], "minScore": 70, "popularityBias": "balanced"},
        }
        token = config.encode_config({"catalogs": [catalog]})

        with self.client() as client, \
            mock.patch.object(
                main.anilist,
                "get_viewer",
                mock.AsyncMock(return_value={"id": 9, "name": "Jordan", "avatar": "https://img.test/avatar.jpg"}),
            ), \
            mock.patch.object(
                main.anilist,
                "get_ai_recommendations",
                mock.AsyncMock(return_value=[make_media(701, "Smart Pick")]),
            ) as get_ai_recommendations, \
            mock.patch.object(main, "batch_map_ids", mock.AsyncMock(return_value=({701: "tt0000701"}, {}))):
            preview = client.post("/api/preview-ai", json={"session": auth_key, "catalog": catalog})
            installed = client.get(f"/{token}~{auth_key}/catalog/series/ai-frieren.json")

        self.assertEqual(preview.status_code, 200)
        self.assertEqual(installed.status_code, 200)
        self.assertEqual(installed.json()["metas"][0]["id"], "tt0000701")
        self.assertEqual(get_ai_recommendations.await_count, 1)

    def test_logout_revokes_durable_auth(self) -> None:
        auth_key = "revoke-me"
        self.create_auth_record(auth_key, with_openrouter=True)

        with self.client() as client:
            logout_response = client.post("/oauth/logout", json={"session": auth_key})
            self.assertEqual(logout_response.status_code, 200)
            self.assertIsNone(self.modules["auth_store"].auth_store.get_auth(auth_key))

            me_response = client.post("/api/me", json={"session": auth_key})
            self.assertEqual(me_response.status_code, 401)

    def test_legacy_cache_auth_migrates_to_sqlite(self) -> None:
        auth_key = "legacy-key"
        cache = self.modules["cache"].cache
        crypto = self.modules["crypto"]
        store = self.modules["auth_store"].auth_store

        cache.set(f"session:{auth_key}", crypto.encrypt("legacy-token"), 3600)
        cache.set(
            f"session_or:{auth_key}",
            {
                "encrypted_key": crypto.encrypt("legacy-openrouter"),
                "model": "openai/gpt-4o-mini",
            },
            3600,
        )
        self.assertIsNone(store.get_auth(auth_key))

        with self.client() as client, \
            mock.patch.object(
                self.modules["main"].anilist,
                "get_viewer",
                mock.AsyncMock(return_value={"id": 11, "name": "Jordan", "avatar": "https://img.test/avatar.jpg"}),
            ):
            response = client.post("/api/me", json={"session": auth_key})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()["has_or_key"])
            self.assertEqual(response.json()["or_model"], "openai/gpt-4o-mini")

            migrated = store.get_auth(auth_key)
            self.assertIsNotNone(migrated)
            self.assertIsNotNone(migrated["encrypted_openrouter_key"])
            self.assertEqual(migrated["openrouter_model"], "openai/gpt-4o-mini")

            cache.clear()
            response = client.post("/api/me", json={"session": auth_key})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()["has_or_key"])

    def test_watching_and_favourites_catalogs_work_after_cache_clear(self) -> None:
        auth_key = "catalog-key"
        self.create_auth_record(auth_key)

        config_token = self.modules["config"].encode_config(
            {
                "catalogs": [
                    {
                        "id": "anilist-watching-current",
                        "name": "Currently Watching",
                        "type": "watching",
                        "listStatus": "CURRENT",
                    },
                    {
                        "id": "anilist-favourites",
                        "name": "My Favourites",
                        "type": "watching",
                        "listStatus": "FAVOURITES",
                    },
                ]
            }
        )
        segment = f"{config_token}~{auth_key}"

        main = self.modules["main"]
        with self.client() as client, \
            mock.patch.object(
                main.anilist,
                "get_viewer",
                mock.AsyncMock(return_value={"id": 15, "name": "Jordan", "avatar": "https://img.test/avatar.jpg"}),
            ), \
            mock.patch.object(
                main.anilist,
                "get_watching_list",
                mock.AsyncMock(return_value=[make_media(111, "Watching Show")]),
            ), \
            mock.patch.object(
                main.anilist,
                "get_favourites",
                mock.AsyncMock(return_value=[make_media(222, "Favourite Show")]),
            ), \
            mock.patch.object(main, "batch_map_ids", mock.AsyncMock(return_value=({}, {}))):
            watching_response = client.get(f"/{segment}/catalog/series/anilist-watching-current.json")
            self.assertEqual(watching_response.status_code, 200)
            self.assertEqual(watching_response.json()["metas"][0]["id"], "anilist:111")

            self.modules["cache"].cache.clear()

            favourites_response = client.get(f"/{segment}/catalog/series/anilist-favourites.json")
            self.assertEqual(favourites_response.status_code, 200)
            self.assertEqual(favourites_response.json()["metas"][0]["id"], "anilist:222")

    def test_public_manifest_and_catalog_remain_unauthenticated(self) -> None:
        config_token = self.modules["config"].encode_config(
            {
                "catalogs": [
                    {
                        "id": "anilist-trending",
                        "name": "Trending Now",
                        "type": "preset",
                    }
                ]
            }
        )
        main = self.modules["main"]
        with self.client() as client, \
            mock.patch.dict(
                main.PRESET_HANDLERS,
                {"anilist-trending": mock.AsyncMock(return_value=[make_media(333, "Trending Show")])},
                clear=False,
            ), \
            mock.patch.object(main, "batch_map_ids", mock.AsyncMock(return_value=({}, {}))):
            manifest_response = client.get(f"/{config_token}/manifest.json")
            self.assertEqual(manifest_response.status_code, 200)
            self.assertEqual(manifest_response.json()["catalogs"][0]["id"], "anilist-trending")

            catalog_response = client.get(f"/{config_token}/catalog/series/anilist-trending.json")
            self.assertEqual(catalog_response.status_code, 200)
            self.assertEqual(catalog_response.json()["metas"][0]["id"], "anilist:333")

    def test_configure_page_contains_poster_lab_label_queries(self) -> None:
        with self.client() as client:
            response = client.get("/configure")

        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("source(version:2)", html)
        self.assertIn("relations{edges{relationType(version:2) node{type}}}", html)
        self.assertIn("Returning Series", html)
        self.assertIn("Recently Adapted", html)
        self.assertIn("Movie Premiere", html)
        self.assertIn("Trending Now", html)

    def test_configure_page_contains_recipe_ui(self) -> None:
        with self.client() as client:
            response = client.get("/configure")

        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("data-action=\"open-share-recipe\"", html)
        self.assertIn("data-action=\"browse-recipes\"", html)
        self.assertIn("recipe-modal-overlay", html)
        self.assertIn("configure?recipe=", html)
        self.assertIn("Shounen Weekend", html)
        self.assertIn("Cozy Slice of Life", html)
        self.assertIn("Current Season No Sequels", html)
        self.assertIn("Share and import public catalog bundles without account or AI auth keys.", html)

    def test_configure_page_contains_smart_rows_ui(self) -> None:
        with self.client() as client:
            response = client.get("/configure")

        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("Smart Rows", html)
        self.assertIn("data-action=\"open-smart-builder\"", html)
        self.assertIn("smart-modal-overlay", html)
        self.assertIn("smart-inline-preview", html)
        self.assertIn("More like my 10/10s", html)
        self.assertIn("Hidden gems from completed", html)
        self.assertIn("id=\"smart-row-note\"", html)
        self.assertNotIn("id=\"smart-or-status\"", html)
        self.assertNotIn("data-action=\"add-ai\"", html)

    def test_static_assets_are_allowlisted(self) -> None:
        with self.client() as client:
            qr_response = client.get("/static/qrcode.min.js")
            font_response = client.get("/static/MonaSansVF.woff2")
            missing_response = client.get("/static/not-shipped.js")

        self.assertEqual(qr_response.status_code, 200)
        self.assertIn("application/javascript", qr_response.headers["content-type"])
        self.assertEqual(font_response.status_code, 200)
        self.assertIn("font/woff2", font_response.headers["content-type"])
        self.assertEqual(missing_response.status_code, 404)

    def test_api_body_and_session_validation_bounds(self) -> None:
        with self.client() as client:
            oversized = client.post(
                "/api/me",
                content=b"x" * 33_000,
                headers={"content-type": "application/json"},
            )
            invalid_session = client.post("/api/me", json={"session": "bad key with spaces"})

        self.assertEqual(oversized.status_code, 413)
        self.assertEqual(invalid_session.status_code, 422)

    def test_config_round_trips_search_custom_catalog(self) -> None:
        config = self.modules["config"]
        catalog = {
            "id": "custom-derived",
            "name": "Completed + Frieren",
            "type": "custom",
            "baseCatalog": {
                "id": "anilist-watching-completed",
                "name": "Completed",
                "type": "watching",
                "listStatus": "COMPLETED",
            },
            "includedMedia": [{"id": 154587, "title": "Frieren: Beyond Journey's End"}],
            "clientFilters": {"genres": ["Adventure"], "minScore": 70},
            "searchSeed": {"id": 154587, "title": "Frieren: Beyond Journey's End"},
            "randomize": True,
        }

        token = config.encode_config({"catalogs": [catalog]})
        decoded = config.decode_config(token)

        self.assertEqual(len(decoded["catalogs"]), 1)
        round_tripped = decoded["catalogs"][0]
        self.assertEqual(round_tripped["type"], "custom")
        self.assertEqual(round_tripped["name"], catalog["name"])
        self.assertEqual(round_tripped["baseCatalog"]["type"], "watching")
        self.assertEqual(round_tripped["baseCatalog"]["listStatus"], "COMPLETED")
        self.assertEqual(round_tripped["includedMedia"][0]["id"], 154587)
        self.assertEqual(round_tripped["searchSeed"]["title"], "Frieren: Beyond Journey's End")
        self.assertEqual(round_tripped["clientFilters"]["genres"], ["Adventure"])
        self.assertTrue(round_tripped["randomize"])

    def test_search_anime_endpoint_enforces_minimum_and_returns_compact_results(self) -> None:
        main = self.modules["main"]

        with self.client() as client:
            short = client.get("/api/search-anime", params={"q": "fr"})
            self.assertEqual(short.status_code, 400)

            with mock.patch.object(
                main.anilist,
                "search_anime",
                mock.AsyncMock(return_value=[make_media(154587, "Frieren: Beyond Journey's End", genres=["Adventure", "Drama"], format="TV", seasonYear=2023)]),
            ) as search_anime:
                response = client.get("/api/search-anime", params={"q": "frie"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["media"][0]["id"], 154587)
        self.assertEqual(payload["media"][0]["title"], "Frieren: Beyond Journey's End")
        self.assertEqual(payload["media"][0]["genres"], ["Adventure", "Drama"])
        self.assertEqual(payload["media"][0]["format"], "TV")
        self.assertEqual(payload["media"][0]["seasonYear"], 2023)
        search_anime.assert_awaited_once()

    def test_custom_catalog_with_base_catalog_and_included_media_requires_auth_and_merges_results(self) -> None:
        auth_key = "derived-custom"
        self.create_auth_record(auth_key)
        config = self.modules["config"]
        main = self.modules["main"]
        catalog = {
            "id": "custom-derived",
            "name": "Completed + Frieren",
            "type": "custom",
            "baseCatalog": {
                "id": "anilist-watching-completed",
                "name": "Completed",
                "type": "watching",
                "listStatus": "COMPLETED",
            },
            "includedMedia": [{"id": 154587, "title": "Frieren: Beyond Journey's End"}],
        }
        token = config.encode_config({"catalogs": [catalog]})

        with self.client() as client:
            unauthenticated = client.get(f"/{token}/catalog/series/custom-derived.json")
            self.assertEqual(unauthenticated.status_code, 401)

        with self.client() as client, \
            mock.patch.object(
                main.anilist,
                "get_viewer",
                mock.AsyncMock(return_value={"id": 42, "name": "Jordan", "avatar": "https://img.test/avatar.jpg"}),
            ), \
            mock.patch.object(
                main.anilist,
                "get_watching_list",
                mock.AsyncMock(return_value=[make_media(111, "Watching Show"), make_media(222, "Another Show")]),
            ), \
            mock.patch.object(
                main.anilist,
                "get_media_by_ids",
                mock.AsyncMock(return_value=[make_media(154587, "Frieren: Beyond Journey's End")]),
            ), \
            mock.patch.object(
                main,
                "batch_map_ids",
                mock.AsyncMock(return_value=({154587: "tt154587", 111: "tt0000111", 222: "tt0000222"}, {})),
            ):
            response = client.get(f"/{token}~{auth_key}/catalog/series/custom-derived.json")

        self.assertEqual(response.status_code, 200)
        metas = response.json()["metas"]
        self.assertEqual(metas[0]["id"], "tt154587")
        self.assertEqual({meta["id"] for meta in metas[:3]}, {"tt154587", "tt0000111", "tt0000222"})


if __name__ == "__main__":
    unittest.main()
