from src.base import find_duplicate_endings, find_unused


def test_find_duplicate_endings(result_items):
    duplicates = find_duplicate_endings(*result_items)
    assert duplicates == [{'apps.core.templatetags.core.profile_tag',
                           'apps.profile.templatetags.profile.profile_tag',
                           'apps.profile.templatetags.user.profile_tag'}]


def test_find_unused(result_items):
    unused, _ = find_unused(*result_items)
    unused.sort()
    assert unused == ['apps.core.shortcuts.short',
                      'apps.profile.shortcuts.short',
                      'apps.profile.templatetags.profile.user_tag']
