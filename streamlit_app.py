import streamlit as st

# Choices and definitions
timeline_choices = [
    ('ASAP ⏱️', 'ASAP', "You need to close as quickly as possible—ideally within weeks—due to relocation, financial needs, or other pressing circumstances. This prioritizes fast options like investor sales or minimal-prep listings, potentially at a trade-off for top dollar."),
    ('Typical 📅', 'Typical', "You're aiming for a standard market timeline, around 1-3 months from listing to close, allowing time for effective marketing and showings without unnecessary delays."),
    ('Flexible 🌟', 'Flexible', "Time is on your side—you’re open to 3+ months if it means strategic enhancements or waiting for the best offer, maximizing value through broader exposure or targeted improvements.")
]
involvement_choices = [
    ('Minimal 🧘', 'Minimal', "You prefer the least disruption possible—limited showings, no major changes to your home, and a hands-off process to keep your daily life uninterrupted."),
    ('Balanced ⚖️', 'Balanced', "You're okay with moderate inconvenience, like occasional showings or light preparations, if it leads to better results without overwhelming your schedule."),
    ('High 🔨', 'High', "You're willing to embrace higher disruption—such as extended access for updates, staging, or more frequent viewings—for the potential of significant ROI and a premium sale price.")
]
condition_choices = [
    ('Needs Work 🛠️', 'Needs Work', "The home hasn’t been cosmetically updated in many years, and likely needs repairs or thorough cleaning due to deferred maintenance. If not already vacant, it may also contain an overabundance of household goods and personal items."),
    ('Marketable 🏡', 'Marketable', "The home has undergone selective improvements in recent years, and is clean and functionally appealing to most buyers. While it is maintained and move-in ready as is, additional enhancements could elevate its presentation to help it compete with newer or renovated homes."),
    ('Showcase ✨', 'Showcase', "The home is either newer construction or recently renovated, and impeccably maintained inside and out. Its contemporary finishes are tasteful and inviting—and might already be staged with the owner's stylish furnishings and curated décor. Its emotionally captivating presentation is media-ready and primed to attract top market attention from discerning buyers.")
]

# Recommendations matrix
recommendations = {
    # Shortened for display; copy your full matrix here!
    ('ASAP', 'Minimal', 'Needs Work'): {
        'primary': 'Cash',
        'primary_desc': "Off-MLS promotion in as-is condition to private investors is the quickest—although usually lower net—option when a home needs more work than a seller is able (or desires) to accomplish.",
        'alt': 'Core',
        'alt_desc': "MLS syndication of pro photos to a wider audience, rather than just investors, will likely increase interest if you're willing to spend some extra time and money for a possibly higher net."
    },
    # ...Paste your entire recommendations dictionary...
}

st.title("SELVO – Home of the Five-Fee Fit™")
st.subheader("Self-Assessment: Which Selvo Listing Tier Fits Me Best?")

with st.expander("Tier Descriptions", expanded=True):
    st.markdown("""
- **(1%) Cash** – Fast, as-is promotion to multiple investors via private network.
- **(2%) Core** – Broad MLS syndication plus essential marketing exposure.
- **(3%) Classic** – Showcase-prep guidance with upgraded media and ad tracking.
- **(4%) Cosmetic** – Advisor-coordinated polishing, updating, and staging.
- **(5%) Comprehensive** – Expert support for strategic ROI-driven renovations.
    """)
    st.write("Percentages (%) apply to Selvo listing services only. While a buyer is responsible for compensating their own agent, their offer may include requesting the seller to offset that amount. This is always optional and negotiable—consult your licensed Selvo agent on the pros and cons.")

def slider_with_expandable_choices(header, choices, slider_key):
    st.markdown(f"#### {header}")
    st.select_slider(
        f"Select your {slider_key.lower()} option:",
        options=[label for label, _, _ in choices],
        value=choices[0][0],
        key=slider_key # stored in st.session_state
    )
    cols = st.columns(3)
    for i, (label, key, desc) in enumerate(choices):
        with cols[i].expander(label, expanded=False):
            st.markdown(desc)

# Show sliders and option boxes with "hidden-until-clicked" definitions
slider_with_expandable_choices("Timeline: How fast would you like to sell your home?", timeline_choices, "Timeline")
slider_with_expandable_choices("Involvement: How much disruption are you willing to tolerate?", involvement_choices, "Involvement")
slider_with_expandable_choices("Condition: What's the current state of your home?", condition_choices, "Condition")

if st.button("Get Recommendation"):
    timeline = st.session_state["Timeline"]
    involvement = st.session_state["Involvement"]
    condition = st.session_state["Condition"]

    # Map selected label to matrix key to look up recommendation
    timeline_key = [key for (label, key, _) in timeline_choices if label == timeline][0]
    involvement_key = [key for (label, key, _) in involvement_choices if label == involvement][0]
    condition_key = [key for (label, key, _) in condition_choices if label == condition][0]
    rec = recommendations.get((timeline_key, involvement_key, condition_key))

    if rec:
        st.success("Your Selvo Sliders Recommendation")
        st.markdown(f"**Primary Option: {rec['primary']}**\n\n{rec['primary_desc']}\n\n**Alternative Option: {rec['alt']}**\n\n{rec['alt_desc']}")
        st.info("Next Steps: Every home and market is unique. [Schedule a free consultation](https://x.ai/grok) with a licensed Selvo agent!")
    else:
        st.error("No recommendation found for this combination.")
