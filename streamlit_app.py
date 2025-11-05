import streamlit as st
import json

# ---------- Brand + Copy ----------
FIVE_FEE = ["Cash (1%)", "Core (2%)", "Classic (3%)", "Cosmetic (4%)", "Comprehensive (5%)"]

intro_md = """
# 🏠 SELVO Five-Fee Fit™ Quiz 🎉
Find the perfect way to sell your home! Slide to match your needs, and we’ll suggest a tailored tier.

**Five Tiers**
- **Cash (1%)** 💸 – Quick investor sale, low hassle.
- **Core (2%)** 📸 – Broad MLS exposure, essentials.
- **Classic (3%)** 🎥 – Upgraded media for appeal.
- **Cosmetic (4%)** 🖌️ – Polishing to shine.
- **Comprehensive (5%)** 🔨 – Full reno for top dollar.

_Percentages are for listing services; buyer-agent fees are negotiable—ask your SELVO agent!_
"""

timeline_choices = [
    ("ASAP ⏱️", "Need to close quickly (weeks)"),
    ("Typical 📅", "Standard pace (1–3 months)"),
    ("Flexible 🌟", "No rush; maximize net (3+ months)")
]
involvement_choices = [
    ("Minimal 🧘", "Prefer low disruption / few showings"),
    ("Balanced ⚖️", "OK with some effort for better results"),
    ("High 🔨", "Willing to invest time/effort for max ROI")
]
condition_choices = [
    ("Needs Work 🛠️", "Not updated; repairs/deep clean likely"),
    ("Marketable 🏡", "Clean, functional, move-in ready"),
    ("Showcase ✨", "Renovated/newer; media-ready")
]

# ---------- Recommendation Logic ----------
overrides = {
    ("ASAP ⏱️", "Minimal 🧘", "Needs Work 🛠️"): {
        "primary": "Cash (1%)",
        "primary_desc": "Fast, off-MLS investor exposure—lowest friction, usually lower net.",
        "alt": "Core (2%)",
        "alt_desc": "MLS + essentials to broaden beyond investors if time allows."
    },
    # Add more overrides as needed
}

def fallback_rule(timeline, involvement, condition):
    if timeline == "ASAP ⏱️" or involvement == "Minimal 🧘" or condition == "Needs Work 🛠️":
        primary = "Cash (1%)" if (timeline == "ASAP ⏱️" and condition != "Marketable 🏡") else "Core (2%)"
        alt = "Core (2%)" if primary == "Cash (1%)" else "Classic (3%)"
        why = "Prioritizes time/certainty and low disruption over maximum price."
        return primary, alt, why
    if timeline == "Flexible 🌟" and involvement == "High 🔨" and condition == "Showcase ✨":
        return "Comprehensive (5%)", "Cosmetic (4%)", "Leans into premium prep & exposure for top outcomes."
    if condition == "Showcase ✨":
        return "Classic (3%)", "Core (2%)", "Great condition—elevated media/placement tends to be enough."
    if condition == "Marketable 🏡":
        return ("Cosmetic (4%)" if involvement == "High 🔨" else "Classic (3%)",
                "Classic (3%)" if involvement == "High 🔨" else "Core (2%)",
                "Targeted polish + tiered media to outperform comps.")
    return "Core (2%)", "Classic (3%)", "Balanced plan for broad exposure with solid media."

primary_desc = {
    "Cash (1%)": "Speed & simplicity; off-MLS investor network minimizes friction.",
    "Core (2%)": "MLS + essential media—broad exposure without extras.",
    "Classic (3%)": "Upgraded media & smarter placement for stronger demand.",
    "Cosmetic (4%)": "Advisor-coordinated polish/staging to outshine comps.",
    "Comprehensive (5%)": "ROI-minded improvements + full campaign to chase peak price."
}

alt_desc = {
    "Core (2%)": "Complementary path if circumstances/market shift.",
    "Classic (3%)": "Complementary path if circumstances/market shift.",
    "Cosmetic (4%)": "Complementary path if circumstances/market shift.",
    "Comprehensive (5%)": "Complementary path if circumstances/market shift.",
    "Cash (1%)": "Complementary path if circumstances/market shift."
}

# ------------- Streamlit UI -------------
st.markdown(intro_md)

def slider_section(title, help, choices):
    st.markdown(f"#### {title}")
    selected = st.select_slider(
        label=help,
        options=[ch[0] for ch in choices],
        value=choices[1][0]  # default to middle
    )
    for label, desc in choices:
        st.markdown(f"- **{label}**: {desc}")
    return selected

timeline = slider_section("Timeline ⏰", "How quickly do you need to close?", timeline_choices)
involvement = slider_section("Involvement ⚙️", "How much disruption can you handle?", involvement_choices)
condition = slider_section("Condition 🏠", "How’s your home looking today?", condition_choices)

st.markdown(f"**Your Choices:** {timeline} • {involvement} • {condition}")

if st.button("Reveal Your SELVO Tier! 🎉"):
    key = (timeline, involvement, condition)
    if key in overrides:
        res = overrides[key]
        primary, alt = res["primary"], res["alt"]
        pdesc, adesc = res["primary_desc"], res["alt_desc"]
        why = "Special-case fit from SELVO’s curated matrix."
    else:
        primary, alt, why = fallback_rule(timeline, involvement, condition)
        pdesc = primary_desc.get(primary, "")
        adesc = alt_desc.get(alt, "")

    st.success(f"**Primary:** {primary}\n\n{pdesc}")
    st.markdown(f"**Alternative:** {alt}\n\n{adesc}")
    st.info(f"_{why}_")
    st.markdown("**Next Steps:** [Schedule a free consultation](http://donotsellyourhouse.com) to tailor your plan! 🚀")
    st.text_area("Copy Your Summary 📋", value=f"""
SELVO Five-Fee Fit™ Recommendation

• Your inputs: {timeline} • {involvement} • {condition}
• Primary: {primary} — {pdesc}
• Alternative: {alt} — {adesc}
Why this fit: {why}
""", height=130)
    st.text_area("JSON Output (for Devs) 💻", value=json.dumps({
        "selections": {
            "timeline": timeline,
            "involvement": involvement,
            "condition": condition
        },
        "primary": {
            "tier": primary,
            "reason": pdesc
        },
        "alternative": {
            "tier": alt,
            "reason": adesc
        },
        "why_this_fit": why
    }, indent=2), height=90)
