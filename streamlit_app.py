import streamlit as st

# -- Define mappings --
timeline_choices = [
    ('ASAP ⏱️', 'ASAP', "You need to close as quickly as possible—ideally within weeks…"),
    ('Typical 📅', 'Typical', "You're aiming for a standard market timeline, around 1-3 months…"),
    ('Flexible 🌟', 'Flexible', "Time is on your side…"),
]
involvement_choices = [
    ('Minimal 🧘', 'Minimal', "You prefer the least disruption possible…"),
    ('Balanced ⚖️', 'Balanced', "You're okay with moderate inconvenience…"),
    ('High 🔨', 'High', "You're willing to embrace higher disruption…"),
]
condition_choices = [
    ('Needs Work 🛠️', 'Needs Work', "The home hasn’t been cosmetically updated in years…"),
    ('Marketable 🏡', 'Marketable', "Home has undergone selective improvements and is move-in ready…"),
    ('Showcase ✨', 'Showcase', "Newer construction or renovated, impeccably maintained…"),
]

# Define the recommendation logic based on the provided 3x3x3 matrix
recommendations = {
    ('ASAP', 'Minimal', 'Needs Work'): {
        'primary': 'Cash',
        'primary_desc': 'Off-MLS promotion in as-is condition to private investors is the quickest—although usually lower net—option when a home needs more work than a seller is able (or desires) to accomplish.',
        'alt': 'Core',
        'alt_desc': 'MLS syndication of pro photos to a wider audience, rather than just investors, will likely increase interest if you\'re willing to spend some extra time and money for a possibly higher net.'
    },
    ('ASAP', 'Minimal', 'Marketable'): {
        'primary': 'Core',
        'primary_desc': 'Although selling to an investor can be quick, a marketable-condition home deserves a chance at a higher offer from a broader buyer pool via limited showing(s) and MLS syndication of pro photos.',
        'alt': 'Cash',
        'alt_desc': 'Investor-only promotion is generally faster than public marketing, though could result in a lower net than a marketable-condition home deserves.'
    },
    ('ASAP', 'Minimal', 'Showcase'): {
        'primary': 'Classic',
        'primary_desc': 'MLS syndication of upgraded media combined with enhanced marketing leverages the emotional appeal of a home in showcase condition.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a home that\'s pristine and desirable.'
    },
    ('ASAP', 'Balanced', 'Needs Work'): {
        'primary': 'Core',
        'primary_desc': 'Marketing "as is" to the general public without fix-up may be sufficient to bring an acceptable offer—and likely higher than promoting it solely to investors.',
        'alt': 'Cosmetic',
        'alt_desc': 'Selective updating plus strategic public marketing adds time, but is less involved than a Comprehensive renovation and will likely improve the buyer pool—as well as the purchase price.'
    },
    ('ASAP', 'Balanced', 'Marketable'): {
        'primary': 'Core',
        'primary_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a marketable-condition home.',
        'alt': 'Classic',
        'alt_desc': 'A marketable-condition home promoted in the MLS with upgraded media and enhanced advertising will likely result in a better offer than Core photos alone.'
    },
    ('ASAP', 'Balanced', 'Showcase'): {
        'primary': 'Classic',
        'primary_desc': 'MLS syndication of upgraded media combined with enhanced marketing leverages the emotional appeal of a home in showcase condition.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a home that\'s pristine and desirable.'
    },
    ('ASAP', 'High', 'Needs Work'): {
        'primary': 'Cosmetic',
        'primary_desc': 'Selective updating plus strategic public marketing adds time, but is less involved than a Comprehensive renovation and will likely improve the buyer pool—as well as the purchase price.',
        'alt': 'Core',
        'alt_desc': 'Marketing to the general public without fix-up may be sufficient to bring an acceptable offer—and likely higher than promoting it solely to investors.'
    },
    ('ASAP', 'High', 'Marketable'): {
        'primary': 'Classic',
        'primary_desc': 'A marketable-condition home promoted with upgraded media and enhanced advertising will likely result in a higher offer than with Core photos alone.',
        'alt': 'Cosmetic',
        'alt_desc': 'If it\'s been awhile since the home was last updated, a selective contemporary refresh could prove worthwhile if time and budget permits.'
    },
    ('ASAP', 'High', 'Showcase'): {
        'primary': 'Classic',
        'primary_desc': 'MLS syndication of upgraded media combined with enhanced marketing leverages the emotional appeal of a home in showcase condition.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a home that\'s pristine and desirable.'
    },
    ('Typical', 'Minimal', 'Needs Work'): {
        'primary': 'Cash',
        'primary_desc': 'As-is, off-MLS promotion to private investors is the least involved—although usually lower net—option when a home needs more work than a seller is able (or desires) to accomplish.',
        'alt': 'Cosmetic',
        'alt_desc': 'If as-is investor offers won\'t meet your goal, selective updating plus strategic public marketing is less involved than a Comprehensive renovation and will likely improve the buyer pool—as well as the purchase price.'
    },
    ('Typical', 'Minimal', 'Marketable'): {
        'primary': 'Classic',
        'primary_desc': 'A marketable-condition home promoted with upgraded media and enhanced advertising will likely result in a higher offer than with Core photos alone.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a marketable-condition home.'
    },
    ('Typical', 'Minimal', 'Showcase'): {
        'primary': 'Classic',
        'primary_desc': 'MLS syndication of upgraded media combined with enhanced marketing leverages the emotional appeal of a home in showcase condition.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a home that\'s pristine and desirable.'
    },
    ('Typical', 'Balanced', 'Needs Work'): {
        'primary': 'Cosmetic',
        'primary_desc': 'Selective updating plus strategic public marketing adds time, but is less involved than a Comprehensive renovation and will likely improve the buyer pool—as well as the purchase price.',
        'alt': 'Comprehensive',
        'alt_desc': 'With enough funds, time, and desire, a thorough renovation is worth considering if the ROI justifies.'
    },
    ('Typical', 'Balanced', 'Marketable'): {
        'primary': 'Classic',
        'primary_desc': 'A marketable-condition home promoted with upgraded media and enhanced advertising will likely result in a higher offer than with Core photos alone.',
        'alt': 'Cosmetic',
        'alt_desc': 'If it\'s been awhile since the home was last updated, a selective contemporary refresh could prove worthwhile if time and budget permits.'
    },
    ('Typical', 'Balanced', 'Showcase'): {
        'primary': 'Classic',
        'primary_desc': 'MLS syndication of upgraded media combined with enhanced marketing leverages the emotional appeal of a home in showcase condition.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a home that\'s pristine and desirable.'
    },
    ('Typical', 'High', 'Needs Work'): {
        'primary': 'Comprehensive',
        'primary_desc': 'With enough funds, time, and desire, a thorough renovation is worth considering if the ROI justifies.',
        'alt': 'Cosmetic',
        'alt_desc': 'Selective updating plus strategic public marketing is less involved than a Comprehensive renovation and will likely improve the buyer pool—as well as the purchase price—over selling as-is.'
    },
    ('Typical', 'High', 'Marketable'): {
        'primary': 'Cosmetic',
        'primary_desc': 'If it\'s been awhile since the home was last updated, a selective contemporary refresh could prove worthwhile if time and budget permits.',
        'alt': 'Comprehensive',
        'alt_desc': 'With enough funds, time, and desire, a thorough renovation is worth considering if the ROI justifies.'
    },
    ('Typical', 'High', 'Showcase'): {
        'primary': 'Classic',
        'primary_desc': 'MLS syndication of upgraded media combined with enhanced marketing leverages the emotional appeal of a home in showcase condition.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a home that\'s pristine and desirable.'
    },
    ('Flexible', 'Minimal', 'Needs Work'): {
        'primary': 'Cash',
        'primary_desc': 'Off-MLS promotion in as-is condition to private investors is the quickest—although usually lower net—option when a home needs more work than a seller is able (or desires) to accomplish.',
        'alt': 'Cosmetic',
        'alt_desc': 'Selective updating plus strategic public marketing is less involved than a Comprehensive renovation and will likely improve the buyer pool—as well as the purchase price—over selling as-is.'
    },
    ('Flexible', 'Minimal', 'Marketable'): {
        'primary': 'Classic',
        'primary_desc': 'A marketable-condition home promoted with upgraded media and enhanced advertising will likely result in a higher offer than with Core photos alone.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a marketable-condition home.'
    },
    ('Flexible', 'Minimal', 'Showcase'): {
        'primary': 'Classic',
        'primary_desc': 'MLS syndication of upgraded media combined with enhanced marketing leverages the emotional appeal of a home in showcase condition.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a home that\'s pristine and desirable.'
    },
    ('Flexible', 'Balanced', 'Needs Work'): {
        'primary': 'Cosmetic',
        'primary_desc': 'Selective updating plus strategic public marketing is less involved than a Comprehensive renovation and will likely improve the buyer pool—as well as the purchase price—over selling as-is.',
        'alt': 'Comprehensive',
        'alt_desc': 'With enough funds, time, and desire, a thorough renovation is worth considering if the ROI justifies.'
    },
    ('Flexible', 'Balanced', 'Marketable'): {
        'primary': 'Classic',
        'primary_desc': 'A marketable-condition home promoted with upgraded media and enhanced advertising will likely result in a higher offer than with Core photos alone.',
        'alt': 'Cosmetic',
        'alt_desc': 'If it\'s been awhile since the home was last updated, a selective contemporary refresh could prove worthwhile if time and budget permits.'
    },
    ('Flexible', 'Balanced', 'Showcase'): {
        'primary': 'Classic',
        'primary_desc': 'MLS syndication of upgraded media combined with enhanced marketing leverages the emotional appeal of a home in showcase condition.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a home that\'s pristine and desirable.'
    },
    ('Flexible', 'High', 'Needs Work'): {
        'primary': 'Comprehensive',
        'primary_desc': 'With enough funds, time, and desire, a thorough renovation is worth considering if the ROI justifies.',
        'alt': 'Cosmetic',
        'alt_desc': 'Selective updating plus strategic public marketing is less involved than a Comprehensive renovation and will likely improve the buyer pool—as well as the purchase price—over selling as-is.'
    },
    ('Flexible', 'High', 'Marketable'): {
        'primary': 'Cosmetic',
        'primary_desc': 'If it\'s been awhile since the home was last updated, a selective contemporary refresh could prove worthwhile if time and budget permits.',
        'alt': 'Comprehensive',
        'alt_desc': 'With enough funds, time, and desire, a thorough renovation is worth considering if the ROI justifies.'
    },
    ('Flexible', 'High', 'Showcase'): {
        'primary': 'Classic',
        'primary_desc': 'MLS syndication of upgraded media combined with enhanced marketing leverages the emotional appeal of a home in showcase condition.',
        'alt': 'Core',
        'alt_desc': 'Pro photos in the MLS plus a limited showing event could suffice for a home that\'s pristine and desirable.'
    }
}

# -- Streamlit UI --

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
    st.write("Percentages (%) apply to Selvo listing services only... (rest of your description here)")

# -- Sliders as select_slider with tooltips --
def choice_label(choices):
    return [f"{name}" for name, key, tooltip in choices]

timeline = st.select_slider(
    "Timeline:",
    options=choice_label(timeline_choices),
    value=choice_label(timeline_choices)[0],
    help="How fast would you like to sell your home?"
)

involvement = st.select_slider(
    "Involvement:",
    options=choice_label(involvement_choices),
    value=choice_label(involvement_choices)[0],
    help="How much disruption are you willing to tolerate?"
)

condition = st.select_slider(
    "Condition:",
    options=choice_label(condition_choices),
    value=choice_label(condition_choices)[0],
    help="What's the current state of your home?"
)

if st.button("Get Recommendation", type="primary"):
    # Look up the mapped values:
    timeline_value = [key for lbl, key, tip in timeline_choices if lbl == timeline][0]
    involvement_value = [key for lbl, key, tip in involvement_choices if lbl == involvement][0]
    condition_value = [key for lbl, key, tip in condition_choices if lbl == condition][0]

    rec = recommendations.get((timeline_value, involvement_value, condition_value))
    if rec:
        st.success("Your Selvo Sliders Recommendation")
        st.markdown(f"**Primary Option: {rec['primary']}**\n\n{rec['primary_desc']}\n\n**Alternative Option: {rec['alt']}**\n\n{rec['alt_desc']}")
        st.info("Next Steps: Every home and market is unique. [Schedule a free consultation](https://x.ai/grok) with a licensed Selvo agent!")
    else:
        st.error("No recommendation found for this combination.")
