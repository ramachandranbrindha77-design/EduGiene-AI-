# EduGenie — Frontend + Backend Demonstration
# Run:
#   pip install gradio
#   python edugenie_app.py
#
# This single file demonstrates:
# FRONT END  -> Gradio tabs, textboxes, dropdowns, buttons, outputs
# BACK END   -> EduGenieLocal class, Q&A, explanation, quiz, summary, learning path

import re
import gradio as gr


# =========================
# BACK END
# =========================

class EduGenieLocal:

    def clean(self, text):
        text = str(text or "").strip()
        return re.sub(r"\s+", " ", text)

    def sentences(self, text):
        text = self.clean(text)
        if not text:
            return []
        return [
            s.strip()
            for s in re.split(r"(?<=[.!?])\s+", text)
            if s.strip()
        ]

    def keywords(self, text):
        stop_words = {
            "the", "is", "are", "was", "were", "a", "an", "and", "or",
            "of", "to", "in", "on", "for", "with", "by", "from", "as",
            "at", "this", "that", "it", "its", "be", "can", "how", "what",
            "why", "when", "where", "which", "who"
        }

        words = re.findall(r"[A-Za-z][A-Za-z0-9_-]*", text.lower())

        result = []
        for word in words:
            if word not in stop_words and len(word) > 2 and word not in result:
                result.append(word)

        return result[:12]

    # ---------- Q&A BACK END ----------
    def answer_question(self, question, context):
        question = self.clean(question)
        context = self.clean(context)

        if not question:
            return "Please enter a question."

        known_answers = {
            "photosynthesis":
                "Photosynthesis is the process by which green plants use sunlight, "
                "carbon dioxide, and water to produce glucose and oxygen.",

            "python":
                "Python is a high-level programming language known for its simple "
                "syntax and wide use in web development, automation, data science, "
                "and artificial intelligence.",

            "artificial intelligence":
                "Artificial Intelligence is the field of creating computer systems "
                "that can perform tasks that normally require human intelligence, "
                "such as learning, reasoning, and understanding language.",

            "machine learning":
                "Machine Learning is a branch of Artificial Intelligence in which "
                "computers learn patterns from data and use those patterns to make "
                "predictions or decisions.",

            "pythagorean theorem":
                "The Pythagorean theorem states that in a right-angled triangle, "
                "a² + b² = c², where c is the hypotenuse.",

            "sql":
                "SQL stands for Structured Query Language. It is used to store, "
                "retrieve, update, and manage data in relational databases.",

            "largest ocean":
                "The Pacific Ocean is the largest ocean on Earth."
        }

        q_lower = question.lower()

        for key, answer in known_answers.items():
            if key in q_lower:
                return answer

        if context:
            context_sentences = self.sentences(context)
            question_words = set(self.keywords(question))
            scored = []

            for sentence in context_sentences:
                sentence_words = set(self.keywords(sentence))
                score = len(question_words.intersection(sentence_words))

                if score > 0:
                    scored.append((score, sentence))

            scored.sort(reverse=True)

            if scored:
                selected = [item[1] for item in scored[:3]]
                return " ".join(selected)

            return "I could not find a direct answer in the provided context."

        return (
            "I can answer common educational questions locally. "
            "For more accurate answers, provide some context or study material."
        )

    # ---------- EXPLAIN BACK END ----------
    def explain(self, topic, level):
        topic = self.clean(topic)

        if not topic:
            return "Please enter a topic."

        explanations = {
            "photosynthesis":
                "Photosynthesis is how green plants make food. Plants use sunlight "
                "as energy and take carbon dioxide from the air and water from the "
                "soil. They produce glucose as food and release oxygen.",

            "python":
                "Python is a programming language designed to be easy to read and "
                "write. It is commonly used for web development, automation, data "
                "analysis, machine learning, and artificial intelligence.",

            "artificial intelligence":
                "Artificial Intelligence allows computers to perform tasks that "
                "usually require human intelligence. Examples include understanding "
                "language, recognizing images, solving problems, and making predictions.",

            "machine learning":
                "Machine Learning allows a computer to learn patterns from examples. "
                "Instead of writing every rule manually, we provide data and the "
                "system learns useful patterns from that data.",

            "sql":
                "SQL is a language used to communicate with relational databases. "
                "You can use SQL to create tables, add information, search information, "
                "change information, and delete information."
        }

        topic_lower = topic.lower()

        for key, explanation in explanations.items():
            if key in topic_lower:
                if level == "Beginner":
                    return explanation

                if level == "Intermediate":
                    return explanation + (
                        "\n\nAt an intermediate level, focus on the main concepts, "
                        "examples, practical applications, and common terminology."
                    )

                return explanation + (
                    "\n\nAt an advanced level, study the underlying algorithms, "
                    "implementation details, limitations, optimization techniques, "
                    "and real-world applications."
                )

        return (
            f"{topic} can be understood by identifying its definition, "
            f"main concepts, examples, applications, and important terms.\n\n"
            f"Learning level: {level}."
        )

    # ---------- SUMMARY BACK END ----------
    def summarize(self, text, length):
        text = self.clean(text)

        if not text:
            return "Please enter text to summarize."

        sentences = self.sentences(text)

        if not sentences:
            return text

        if length == "Short":
            count = 2
        elif length == "Medium":
            count = 4
        else:
            count = 6

        if len(sentences) <= count:
            return " ".join(sentences)

        words = self.keywords(text)
        scored = []

        for index, sentence in enumerate(sentences):
            sentence_words = set(self.keywords(sentence))
            score = len(sentence_words.intersection(words))
            scored.append((score, index, sentence))

        scored.sort(key=lambda x: (-x[0], x[1]))

        selected = sorted(scored[:count], key=lambda x: x[1])
        return " ".join(item[2] for item in selected)

    # ---------- QUIZ BACK END ----------
    def quiz(self, topic, number):
        topic = self.clean(topic)

        if not topic:
            return "Please enter a topic."

        question_bank = {
            "python": [
                (
                    "What type of language is Python?",
                    ["Programming language", "Database", "Operating system", "Browser"],
                    "Programming language"
                ),
                (
                    "Which symbol is commonly used to start a comment in Python?",
                    ["#", "$", "@", "&"],
                    "#"
                ),
                (
                    "Which data type stores multiple values in an ordered collection?",
                    ["List", "Integer", "Boolean", "Float"],
                    "List"
                )
            ],

            "photosynthesis": [
                (
                    "What is the main energy source for photosynthesis?",
                    ["Sunlight", "Soil", "Oxygen", "Nitrogen"],
                    "Sunlight"
                ),
                (
                    "Which gas do plants take in during photosynthesis?",
                    ["Carbon dioxide", "Oxygen", "Hydrogen", "Helium"],
                    "Carbon dioxide"
                ),
                (
                    "What gas is released during photosynthesis?",
                    ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"],
                    "Oxygen"
                )
            ],

            "artificial intelligence": [
                (
                    "What does AI stand for?",
                    ["Artificial Intelligence", "Automatic Internet",
                     "Advanced Input", "Artificial Information"],
                    "Artificial Intelligence"
                ),
                (
                    "Which field allows computers to learn patterns from data?",
                    ["Machine Learning", "Networking",
                     "Operating Systems", "Database Design"],
                    "Machine Learning"
                )
            ],

            "machine learning": [
                (
                    "What is the main idea of Machine Learning?",
                    ["Learning patterns from data", "Only storing files",
                     "Designing websites", "Creating hardware"],
                    "Learning patterns from data"
                ),
                (
                    "Machine Learning is a branch of which field?",
                    ["Artificial Intelligence", "Networking",
                     "Cybersecurity", "Operating Systems"],
                    "Artificial Intelligence"
                )
            ]
        }

        topic_lower = topic.lower()
        selected_bank = None

        for key, bank in question_bank.items():
            if key in topic_lower:
                selected_bank = bank
                break

        if selected_bank is None:
            selected_bank = [
                (
                    f"What is an important way to study {topic}?",
                    ["Understand concepts", "Avoid practice",
                     "Ignore examples", "Skip revision"],
                    "Understand concepts"
                ),
                (
                    f"What can help you learn {topic} better?",
                    ["Practice", "Never review",
                     "Avoid questions", "Ignore mistakes"],
                    "Practice"
                )
            ]

        number = int(number)
        selected_questions = selected_bank[:number]
        output = []

        for index, item in enumerate(selected_questions, start=1):
            question, options, answer = item

            output.append(
                f"Question {index}: {question}\n"
                f"A. {options[0]}\n"
                f"B. {options[1]}\n"
                f"C. {options[2]}\n"
                f"D. {options[3]}\n"
                f"Answer: {answer}"
            )

        return "\n\n".join(output)

    # ---------- LEARNING PATH BACK END ----------
    def learning_path(self, topic, level):
        topic = self.clean(topic)

        if not topic:
            return "Please enter a topic."

        return (
            f"Learning Path for: {topic}\n\n"
            f"Level: {level}\n\n"
            "Step 1: Learn the basic definition and terminology.\n"
            "Step 2: Understand the core concepts.\n"
            "Step 3: Study simple examples.\n"
            "Step 4: Practice questions and exercises.\n"
            "Step 5: Work on a small practical project.\n"
            "Step 6: Review mistakes and weak areas.\n"
            "Step 7: Move to advanced concepts."
        )


# =========================
# FRONT END
# =========================

engine = EduGenieLocal()

CUSTOM_CSS = """
.gradio-container {
    max-width: 1100px !important;
    margin: auto !important;
}

.hero {
    text-align: center;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 17px;
}

.section-title {
    font-size: 22px;
    font-weight: bold;
}
"""


with gr.Blocks(
    title="EduGenie - Learning Assistant",
    css=CUSTOM_CSS
) as demo:

    # HOME / HEADER
    gr.HTML("""
    <div class="hero">
        <h1>🎓 EduGenie</h1>
        <p><b>AI-Inspired Local Learning Assistant</b></p>
        <p>
            Ask questions • Learn concepts • Generate quizzes •
            Summarize notes • Build learning paths
        </p>
    </div>
    """)

    # FRONTEND DEMONSTRATION
    with gr.Tab("🏠 Home"):
        gr.Markdown("""
        ## Welcome to EduGenie

        EduGenie is an educational assistant demonstrating a complete
        **frontend + backend architecture** in one Python project.

        ### Front End
        - User interface created with Gradio
        - Tabs and input forms
        - Buttons and output areas
        - Learning-level controls

        ### Back End
        - Question answering
        - Topic explanation
        - Text summarization
        - Quiz generation
        - Personalized learning path

        ### Demo Flow

        **Student → Front End → Python Backend → Processing → Result**
        """)

    # Q&A
    with gr.Tab("💬 Q&A"):
        question = gr.Textbox(
            label="Question",
            placeholder="Example: What is photosynthesis?"
        )

        context = gr.Textbox(
            label="Study Context",
            placeholder="Paste your study material here...",
            lines=8
        )

        answer_button = gr.Button("Get Answer", variant="primary")

        answer_output = gr.Textbox(
            label="Backend Response",
            lines=8
        )

        answer_button.click(
            engine.answer_question,
            inputs=[question, context],
            outputs=answer_output
        )

    # EXPLAIN
    with gr.Tab("📚 Explain"):
        topic = gr.Textbox(
            label="Topic",
            placeholder="Example: Python"
        )

        level = gr.Dropdown(
            ["Beginner", "Intermediate", "Advanced"],
            value="Beginner",
            label="Learning Level"
        )

        explain_button = gr.Button(
            "Explain Topic",
            variant="primary"
        )

        explanation_output = gr.Textbox(
            label="Explanation",
            lines=10
        )

        explain_button.click(
            engine.explain,
            inputs=[topic, level],
            outputs=explanation_output
        )

    # QUIZ
    with gr.Tab("📝 Quiz"):
        quiz_topic = gr.Textbox(
            label="Quiz Topic",
            placeholder="Example: Python"
        )

        quiz_number = gr.Slider(
            minimum=1,
            maximum=5,
            value=3,
            step=1,
            label="Number of Questions"
        )

        quiz_button = gr.Button(
            "Generate Quiz",
            variant="primary"
        )

        quiz_output = gr.Textbox(
            label="Generated Quiz",
            lines=15
        )

        quiz_button.click(
            engine.quiz,
            inputs=[quiz_topic, quiz_number],
            outputs=quiz_output
        )

    # SUMMARY
    with gr.Tab("📄 Summary"):
        summary_text = gr.Textbox(
            label="Study Text",
            placeholder="Paste the text you want to summarize...",
            lines=12
        )

        summary_length = gr.Dropdown(
            ["Short", "Medium", "Long"],
            value="Medium",
            label="Summary Length"
        )

        summary_button = gr.Button(
            "Summarize",
            variant="primary"
        )

        summary_output = gr.Textbox(
            label="Summary",
            lines=10
        )

        summary_button.click(
            engine.summarize,
            inputs=[summary_text, summary_length],
            outputs=summary_output
        )

    # LEARNING PATH
    with gr.Tab("🛤️ Learning Path"):
        path_topic = gr.Textbox(
            label="Topic",
            placeholder="Example: Machine Learning"
        )

        path_level = gr.Dropdown(
            ["Beginner", "Intermediate", "Advanced"],
            value="Beginner",
            label="Level"
        )

        path_button = gr.Button(
            "Create Learning Path",
            variant="primary"
        )

        path_output = gr.Textbox(
            label="Learning Path",
            lines=12
        )

        path_button.click(
            engine.learning_path,
            inputs=[path_topic, path_level],
            outputs=path_output
        )

    gr.Markdown("""
    ---
    **EduGenie Project Demonstration**

    Frontend: Gradio UI  
    Backend: Python `EduGenieLocal` class  
    Architecture: User Input → Backend Processing → Educational Output
    """)


if __name__ == "__main__":
    demo.launch(share=True)
