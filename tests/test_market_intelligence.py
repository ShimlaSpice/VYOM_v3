"""
Test Market Intelligence Providers.
"""

from app.market import (
    GlobalMarketProvider,
    FIIDIIProvider,
    CorporateActionProvider,
    InsiderActivityProvider,
)


def main():

    print("=" * 80)
    print("GLOBAL MARKETS")
    print("=" * 80)

    global_data = GlobalMarketProvider().fetch()

    for key, value in global_data.items():

        print(f"{key:20}: {value}")

    print()

    print("=" * 80)
    print("FII / DII")
    print("=" * 80)

    fii = FIIDIIProvider().fetch()

    print(fii)

    print()

    print("=" * 80)
    print("CORPORATE ACTIONS")
    print("=" * 80)

    corporate = CorporateActionProvider().fetch(

        "RELIANCE.NS",

    )

    print(corporate)

    print()

    print("=" * 80)
    print("INSIDER ACTIVITY")
    print("=" * 80)

    insider = InsiderActivityProvider().fetch(

        "RELIANCE.NS",

    )

    print(insider)


if __name__ == "__main__":

    main()