def generate_sample_data():
    title = "Effectiveness of New Drug X in Treating Hypertension"

    context_objectives = """This study aims to evaluate the effectiveness of New Drug X in reducing blood
    pressure levels in patients diagnosed with hypertension.
    """

    population = """The study involves 500 participants aged between 30 and 65,
    all diagnosed with stage 1 or stage 2 hypertension. Participants were randomly
    assigned to either the treatment group receiving New Drug X or the control
    group receiving a placebo.
    """

    methods = """A double-blind, randomized, placebo-controlled trial was conducted
    over 12 weeks. Blood pressure levels were measured at baseline, week 6, and week 12.
    Statistical analysis was performed using a mixed-effects model for repeated measures.
    """

    abstracts = [
        "Abstract 1: Previous studies have shown that Drug A significantly reduces systolic \
        and diastolic blood pressure in hypertensive patients. \
        However, the long-term effects of Drug A remain unclear.",
        "Abstract 2: The impact of Drug B on blood pressure variability was assessed in a \
        randomized controlled trial involving 300 hypertensive patients. \
        Results indicated a notable reduction in blood pressure fluctuations over a 24-hour period.",
        "Abstract 3: A comparative study between Drug C and Drug D demonstrated that both \
        medications effectively lower blood pressure, with Drug C showing a slightly \
        better safety profile in elderly patients.",
    ]

    abstracts_str = "\n\n".join(abstracts)

    keyresults = ""
    keywords = ""
    ethics = ""

    return (
        title,
        context_objectives,
        population,
        methods,
        abstracts_str,
        keyresults,
        keywords,
        ethics,
    )