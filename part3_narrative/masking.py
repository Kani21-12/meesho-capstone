def alias_for(reseller_id: str) -> str:
    """
    Convert an internal reseller ID into an external-safe alias.

    Example:
        RS019 -> ALIAS-19
        RS006 -> ALIAS-06
    """
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """
    Return False if any raw reseller name appears in the text.

    The check is a direct substring search so that even a name appearing
    inside a larger sentence is detected.
    """
    for reseller_name in reseller_names:
        if reseller_name in text:
            return False

    return True


if __name__ == "__main__":
    reseller_names = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5",
    ]

    safe_narrative = (
        "FACT: West ALIAS-19 and West ALIAS-22 are among the top reseller accounts. "
        "South ALIAS-12, North ALIAS-06, and North ALIAS-05 are also included."
    )

    unsafe_narrative = (
        "FACT: Mumbai Reseller 1 is among the top reseller accounts."
    )

    print("===== MASKING TESTS =====")

    print(
        "alias_for('RS019'):",
        alias_for("RS019")
    )

    print(
        "alias_for('RS006'):",
        alias_for("RS006")
    )

    safe_result = assert_no_raw_names_leak(
        safe_narrative,
        reseller_names
    )

    unsafe_result = assert_no_raw_names_leak(
        unsafe_narrative,
        reseller_names
    )

    print("Safe narrative:", safe_result)
    print("Unsafe narrative:", unsafe_result)

    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"

    assert safe_result is True
    assert unsafe_result is False

    print("All masking tests passed.")