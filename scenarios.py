"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "I am very busy and frustrated with these days because I have some many interviews and busy with preparation for them, but yet I didn't get any offer.",
            "I have been looking for data scientist job for around one year and I have 10 years experiences"
            
        ],
    },
    {
        "name": "label coverage",
        "criterion": 5,
        # Inputs spread across your score range, so you can check all three
        # labels are actually reachable.
        "texts": [
            "A strong work ethic has been the most important to both my academic and professional achievements. During my Ph.D. research in physics, I worked on complex computational and experimental problems that required persistence, attention to detail, and the ability to learn new methods independently.",
            "I love physics but I have to turn to data science field because with physics it is hard to get a descent job.",
            "I strongly believe my these experience will directly help advance the President's Executive Orders and policy priorities in this roleto improve efficiency and effectiveness of Consumer Product Safety Commission.",
        ],
    },
    {
        "name": "false negatives (AI text called human)",
        "criterion": 2,
        # Text that is plainly machine-written. Criterion 2 allows at most 1 of
        # these 5 to come back labelled high-confidence human.
        "texts": [
            "The importance of effective time management cannot be overstated in today's fast-paced work environment. Professionals who develop strong organizational habits are better positioned to meet deadlines and reduce stress. There are several key strategies that can help individuals improve their productivity. First, prioritization is essential. By identifying the most important tasks and addressing them first, workers can ensure that critical objectives are met. Second, minimizing distractions plays a significant role. Setting aside dedicated blocks of time for concentrated work is widely considered beneficial. Finally, regular breaks are important for maintaining performance.",
            "Data science has emerged as one of the most transformative fields of the modern era. It combines statistics, computer science, and domain expertise to extract meaningful insights from large volumes of data. Organizations across every industry now rely on data-driven decision making to remain competitive. As the volume of available data continues to grow, the demand for skilled practitioners is expected to increase accordingly.",
            "Regular physical exercise offers numerous benefits for both physical and mental health. It strengthens the cardiovascular system, improves muscular endurance, and helps maintain a healthy body weight. In addition, exercise has been shown to reduce symptoms of anxiety and depression. Experts generally recommend at least 150 minutes of moderate activity per week for adults.",
            "Effective communication is a cornerstone of successful teamwork. When team members share information clearly and listen actively, misunderstandings are reduced and projects move forward more efficiently. Leaders play a particularly important role by setting expectations, providing constructive feedback, and fostering an environment in which every member feels comfortable contributing.",
            "Climate change represents one of the most significant challenges facing humanity today. Rising global temperatures contribute to more frequent extreme weather events, rising sea levels, and disruptions to agricultural systems. Addressing this challenge requires coordinated action at the international, national, and local levels, including a transition toward renewable energy sources.",
        ],
    },
    {
        "name": "score spread (clearly human vs clearly AI)",
        "criterion": 3,
        # Matched pairs: the first three are messy, specific, first-person human
        # prose; the last three are smooth generic machine prose. Criterion 3
        # asks that the human mean and the AI mean land at least 0.2 apart.
        "texts": [
            "I didn't sleep. Not properly, anyway - I lay there listening to the boiler tick and thinking about the thing I'd said to Marcus at the pub, which was stupid, and which he will absolutely bring up again. Twice now. So: coffee, and the long way round to work, and a plan. The plan lasted until about ten past nine.",
            "My laptop fan started screaming halfway through the fit, so I killed the kernel, made tea, and came back to find I'd been training on the wrong column the entire afternoon. Four hours. The target was sitting right there in the features. Honestly I laughed.",
            "Ten years of physics and the thing I miss most is not the equations, it's the smell of the lab at 2am when the cryostat finally stabilises and nobody else is in the building. Nobody tells you that part when you switch fields.",
            "In conclusion, the adoption of renewable energy technologies offers substantial long-term benefits for both the environment and the economy. Governments, businesses, and individuals all have important roles to play in this transition. By working together, society can build a more sustainable future for generations to come.",
            "Machine learning models require careful evaluation before deployment. Practitioners should consider multiple metrics, validate performance on held-out data, and monitor for distribution shift over time. A thoughtful evaluation process helps ensure that models perform reliably in real-world conditions.",
            "Developing strong study habits is essential for academic success. Students who create consistent schedules, review material regularly, and seek help when needed tend to achieve better outcomes. It is also important to maintain a healthy balance between academic work and personal well-being.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 4,
        # Raw request bodies, sent exactly as written. Criterion 4 asks that each
        # of these comes back as an explicit input error, not a guessed label.
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},            # no text field at all
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": " " * 20, "creator_id": "eval_bad_whitespace"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
            {"text": 12345, "creator_id": "eval_bad_wrongtype"},
        ],
    },

    # NOTE: criterion 5 (label coverage) is the "label coverage" scenario above.
    # Criterion 4's appeal half, if you make one, can't be tested by sending
    # text alone: it needs a submission first and then an appeal against the
    # content_id that came back. Test that by hand and say so in the write-up.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
