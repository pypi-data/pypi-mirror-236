# TODO these are not functional until feature flags are supported.
# import logging
# from typing import Tuple
#
# import pytest
# from pytest_mock import MockerFixture
# from sqlalchemy.orm.session import Session
#
# from CAP.database.models.platform.feature_flag import FeatureFlag
# from CAP.platform import DBFeatureFlagRouter
#
# _FEATURE_FLAG_TEST_NAME = "foo_feature"
# _FEATURE_FLAG_TEST_DESCRIPTION = "foo description"
#
#
# def _create_feature_flag(session: Session):
#    session.add(
#        FeatureFlag(
#            name=_FEATURE_FLAG_TEST_NAME, description=_FEATURE_FLAG_TEST_DESCRIPTION
#        )
#    )
#    session.commit()
#
#
# def test__feature_is_enabled__defaults_to_false(session: Session, set_up_database):
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session, logger)
#    _create_feature_flag(session)
#
#    # The value is false because it was not explicitly enabled. This is the database default value.
#    is_enabled = db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME)
#
#    assert is_enabled == False
#
#
# def test__feature_is_enabled__defaults_to_false_when_flag_does_not_exist(
#    session: Session, set_up_database
# ):
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session, logger)
#
#    is_enabled = db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME)
#
#    assert is_enabled == False
#
#
# def test__feature_is_enabled__disallows_empty_name(session: Session):
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session, logger)
#
#    with pytest.raises(ValueError):
#        db_feature_flag_router.feature_is_enabled("")
#
#
# @pytest.mark.parametrize("name", [0, False, True, {}, [], (0,)])
# def test__feature_is_enabled__disallows_non_string_names(name, session: Session):
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session, logger)
#
#    with pytest.raises(TypeError):
#        db_feature_flag_router.feature_is_enabled(name)
#
#
# def test__set_feature_is_enabled__fails_when_flag_does_not_exist(
#    session: Session, set_up_database
# ):
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session, logger)
#
#    with pytest.raises(LookupError):
#        db_feature_flag_router.set_feature_is_enabled(_FEATURE_FLAG_TEST_NAME, True)
#
#
# def test__set_feature_is_enabled__disallows_empty_name(session: Session):
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session, logger)
#    _create_feature_flag(session)
#
#    with pytest.raises(ValueError):
#        db_feature_flag_router.set_feature_is_enabled("", False)
#
#
# @pytest.mark.parametrize("name", [0, False, True, {}, [], (0,)])
# def test__set_feature_is_enabled__disallows_non_string_names(name, session: Session):
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session, logger)
#
#    with pytest.raises(TypeError):
#        db_feature_flag_router.set_feature_is_enabled(name, False)
#
#
# @pytest.mark.parametrize("enable", [True, False])
# def test__set_feature_is_enabled__sets_correct_value(
#    enable: bool, session: Session, set_up_database
# ):
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session, logger)
#    _create_feature_flag(session)
#
#    db_feature_flag_router.set_feature_is_enabled(_FEATURE_FLAG_TEST_NAME, enable)
#    is_enabled = db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME)
#
#    assert is_enabled == enable
#
#
# @pytest.mark.parametrize("enable", [True, False])
# def test__set_feature_is_enabled__caches_flags(enable: bool, mocker: MockerFixture):
#    session_mock = mocker.patch("sqlalchemy.orm.session.Session")
#    session_query_mock = mocker.patch("sqlalchemy.orm.session.Session.query")
#    session_mock.query = session_query_mock
#
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session_mock, logger)
#
#    db_feature_flag_router.set_feature_is_enabled(_FEATURE_FLAG_TEST_NAME, enable)
#    db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME)
#    db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME)
#
#    assert session_query_mock.call_count == 1
#
#
# @pytest.mark.parametrize("check_cache", [(True, 1), (False, 0)])
# def test__feature_is_enabled__checks_cache(
#    check_cache: Tuple[bool, int], mocker: MockerFixture
# ):
#    session_mock = mocker.patch("sqlalchemy.orm.session.Session")
#    feature_is_enabled_mock = mocker.patch(
#        "CAP.platform.feature_flag_router.FeatureFlagRouter.feature_is_enabled"
#    )
#    set_feature_is_enabled_mock = mocker.patch(
#        "CAP.platform.feature_flag_router.FeatureFlagRouter.set_feature_is_enabled"
#    )
#
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session_mock, logger)
#
#    db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME, check_cache[0])
#
#    assert feature_is_enabled_mock.call_count == check_cache[1]
#
#
# @pytest.mark.parametrize("check_cache", [(True, 0), (False, 1)])
# def test__feature_is_enabled__sets_cache(
#    check_cache: Tuple[bool, int], mocker: MockerFixture
# ):
#    session_mock = mocker.patch("sqlalchemy.orm.session.Session")
#    feature_is_enabled_mock = mocker.patch(
#        "CAP.platform.feature_flag_router.FeatureFlagRouter.feature_is_enabled"
#    )
#    set_feature_is_enabled_mock = mocker.patch(
#        "CAP.platform.feature_flag_router.FeatureFlagRouter.set_feature_is_enabled"
#    )
#    feature_is_enabled_mock.return_value = True
#
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session_mock, logger)
#
#    db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME, check_cache[0])
#
#    assert set_feature_is_enabled_mock.call_count == check_cache[1]
#
#
# @pytest.mark.parametrize("enable", [True, False])
# def test__set_feature_is_enabled__resets_cache_when_flag_enable_is_set(
#    enable: bool, mocker: MockerFixture
# ):
#    session_mock = mocker.patch("sqlalchemy.orm.session.Session")
#    session_query_mock = mocker.patch("sqlalchemy.orm.session.Session.query")
#    session_mock.query = session_query_mock
#
#    logger = logging.getLogger("FeatureFlagLogger")
#    db_feature_flag_router = DBFeatureFlagRouter(session_mock, logger)
#
#    db_feature_flag_router.set_feature_is_enabled(_FEATURE_FLAG_TEST_NAME, enable)
#    db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME)
#    first_value = db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME)
#
#    db_feature_flag_router.set_feature_is_enabled(_FEATURE_FLAG_TEST_NAME, not enable)
#    db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME)
#    second_value = db_feature_flag_router.feature_is_enabled(_FEATURE_FLAG_TEST_NAME)
#
#    assert session_query_mock.call_count == 2
#    assert first_value == enable
#    assert second_value == (not enable)
#
