import pandas as pd
    • Scale bundled Health + Term creators
    """)

    st.divider()

    st.subheader("Budget Reallocation Simulator")

    budget_shift = st.slider(
        "Increase Top Creator Budget (%)",
        0,
        50,
        20
    )

    projected_roi = 3.2 + (budget_shift * 0.03)

    st.metric(
        "Projected ROI",
        f"{projected_roi:.2f}x"
    )

    st.divider()

    if st.button("Generate Founder Recommendations"):

        st.toast("Top creators identified for scale allocation")

        st.success("""
        Recommended Next Actions

        • Increase allocation toward LinkedIn creators.

        • Reduce low efficiency creator spend.

        • Expand bundled insurance campaigns.

        • Improve SLA tracking before scaling outreach.
        """)

    st.divider()

    st.subheader("Strategic Operating Notes")

    st.info("""
    • LinkedIn creators continue delivering strongest blended ROI.

    • Repeat creators materially outperform one-off activations.

    • Attribution consistency remains the biggest operational bottleneck.

    • Dedicated YouTube should be treated selectively as awareness inventory.
    """)
