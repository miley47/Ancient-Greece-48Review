from flask import Flask, render_template, request, session, redirect, url_for
import random
app = Flask(__name__)
app.secret_key = "48review-greece-local-test-key"

QUESTIONS = [('THIS IS WHERE THE OLYMPIC GAMES WERE HELD EVERY 4 YEARS TO HONOUR THE GODS.', 'OLYMPIA'), ('HIGH HILL IN ATHENS WHERE THE TEMPLES WERE BUILT.', 'ACROPOLIS'), ('GOVERNMENT BY A FEW STRONG FAMILIES.', 'OLIGARCHY'), ("ATHENA'S MAIN TEMPLE ON THE ACROPOLIS.", 'PARTHENON'), ('WHAT THE GREEKS CALLED GREECE.', 'HELLAS'), ('FAMOUS GREEK PHILOSOPHER. HE TAUGHT ALEXANDER THE GREAT. HE WROTE ABOUT JUST ABOUT EVERYTHING.', 'ARISTOTLE'), ('GEOGRAPHICAL PLAIN UPON WHICH ATHENS IS FOUND.', 'ATTICA'), ('IT MEANS A MAIN CITY, NEW YORK, TORONTO ETC.', 'METROPOLIS'), ('IT MEANS MANY.', 'POLY'), ('THE FIRST GREEK LETTER.', 'ALPHA'), ('5TH CENTURY LEADER OF THE ATHENIANS. OLD ONION HEAD.', 'PERICLES'), ('MOUNTAIN HOME OF THE GREEK GODS', 'OLYMPUS'), ('COUNTRY OF DARIUS AND XERCES WHO INVADED THE GREEK HOMELAND. PRESENT DAY IRAN.', 'PERSIA'), ('KING OF THE GREEK GODS', 'ZEUS'), ('ATHENIAN COUNCIL CHOSEN BY LOT FROM CITIZENRY', 'BOULE'), ('A MAN', 'HOMO'), ('THE SEA AROUND WHICH MOST GREEKS LIVED', 'AEGEAN'), ('HILL ON WHICH THE ATHENIAN MALES WOULD MEET TO DISCUSS POLITICS.', 'PYNX'), ('GREEK LETTER FOR P.', 'PI'), ('THE GENERALS WHO LED THE ATHENIANS.', 'STRATEGOI'), ("THE ATHENIAN'S CITIZEN ASSEMBLY.", 'ECCLESIA'), ('A CITY STATE.', 'POLIS'), ('A GREEK MARKET PLACE.', 'AGORA'), ('AN ATHENIAN WAR SHIP WITH 3 ROWS OF OARS.', 'TRIREME'), ('LOVE OF WISDOM OR PURSUIT OF KNOWLEDGE.', 'PHILOSOPHY'), ('BELIEF IN MANY GODS.', 'POLYTHEISM'), ('A TEACHER OF CHILDREN.', 'PEDAGOGUE'), ('ATHENIAN FORM OF GOVERNMENT WHERE POWER WAS IN THE HANDS OF THE PEOPLE.', 'DEMOCRACY'), ('A GREEK CITY STATE WHICH OPPOSED ATHENS.', 'SPARTA'), ('"I FOUND IT!" IN GREEK, YELLED BY ARCHIMEDES RUNNING FROM HIS BATHTUB.', 'EUREKA'), ('IT MEANS ONE.', 'MONO'), ('GREEK LETTER FOR I. IT MEANS A TINY LITTLE BIT IN ENGLISH.', 'IOTA'), ('A PLACE FOR WOMEN ONLY.', 'GYNAECIUM'), ('GREEK WORD FOR VICTORY.', 'NIKE'), ('HE TOLD STORIES LIKE, THE HARE AND THE TURTLE, THE FROG AND THE BULL ETC.', 'AESOP'), ("HOMER'S STORY ABOUT ODYSSEUS JOURNEY AFTER THE TROJAN WAR.", 'ODYSSEY'), ('VICTORY WON BY ATHENIANS OVER THE PERSIANS.', 'MARATHON'), ('THE FAVOURITE GODDESS OF ATHENS. GODDESS OF WISDOM.', 'ATHENA'), ('GREAT CONQUEROR WHO SPREAD GREEK POWER ALL THE WAY TO INDIA, BUT HE DIED A YOUNG MAN.', 'ALEXANDER'), ('AN ARTISAN IN ATHENS WITHOUT VOTING RIGHTS.', 'METIC'), ('GOVERNMENT BY ONE WHO TAKES POWER ILLEGALLY.', 'TYRANNY'), ('IT MEANS FIVE.', 'PENT'), ('NAME OF THE GREEK LEAGUE AGAINST THE PERSIANS.', 'DELIAN'), ('A SIMPLE GREEK COLUMN. OTHERS WERE IONIC OR CORINTHIAN.', 'DORIC'), ('A GREEK PHILOSOPHER WHOSE TEACHING METHOD WAS BASED ON QUESTIONING.', 'SOCRATES'), ('THE LAST GREEK LETTER.', 'OMEGA'), ('THE GREEK SYSTEM OF LETTERS.', 'ALPHABET'), ('THE GREAT RELIGIOUS FESTIVAL HELD ON THE ACROPOLIS TO HONOR ATHENA.', 'PANATHENEA')]
ORIGINAL_ORDER = [10, 33, 4, 5, 37, 13, 47, 36, 19, 7, 17, 20, 25, 2, 45, 6, 21, 46, 16, 3, 41, 24, 27, 26, 42, 43, 22, 15, 32, 34, 14, 18, 12, 38, 39, 9, 44, 29, 23, 35, 40, 8, 31, 30, 28, 48, 11, 1]
WORDS = [answer for clue, answer in QUESTIONS]

def start_game():
    session.clear()
    session["remaining"] = ORIGINAL_ORDER.copy()
    random.shuffle(session["remaining"])
    session["checked"] = []
    session["score_numerator"] = 48
    session["score_denominator"] = 48
    session["feedback"] = ""
    session["selected"] = None
    session["correct_selected"] = False

@app.route("/")
def index():
    if "remaining" not in session:
        start_game()

    if not session["remaining"]:
        pct = 100 * session["score_numerator"] / session["score_denominator"]
        return render_template(
            "index.html",
            finished=True,
            score_numerator=session["score_numerator"],
            score_denominator=session["score_denominator"],
            percentage=f"{pct:.2f}",
            clue="",
            choices=[],
            feedback="",
            selected=None,
            correct_selected=False
        )

    q_index = session["remaining"][0] - 1
    clue, correct = QUESTIONS[q_index]
    pct = 100 * session["score_numerator"] / session["score_denominator"]

    return render_template(
        "index.html",
        finished=False,
        score_numerator=session["score_numerator"],
        score_denominator=session["score_denominator"],
        percentage=f"{pct:.2f}",
        clue=clue,
        choices=WORDS,
        checked=session.get("checked", []),
        feedback=session.get("feedback", ""),
        selected=session.get("selected"),
        correct_selected=session.get("correct_selected", False)
    )

@app.route("/answer", methods=["POST"])
def answer():
    if not session.get("remaining"):
        return redirect(url_for("index"))

    selected = request.form.get("answer", "")
    q_index = session["remaining"][0] - 1
    _, correct = QUESTIONS[q_index]

    if selected == correct:
        session["feedback"] = ""
        session["selected"] = selected
        session["correct_selected"] = True
        checked = session.get("checked", [])
        if q_index not in checked:
            checked.append(q_index)
            session["checked"] = checked
    else:
        session["score_denominator"] += 1
        session["feedback"] = "NO, SORRY, THAT'S NOT IT, TRY AGAIN."
        session["selected"] = selected
        session["correct_selected"] = False

    return redirect(url_for("index"))

@app.route("/next", methods=["POST"])
def next_question():
    if session.get("correct_selected") and session.get("remaining"):
        session["remaining"] = session["remaining"][1:]
    session["feedback"] = ""
    session["selected"] = None
    session["correct_selected"] = False
    return redirect(url_for("index"))

@app.route("/restart", methods=["POST"])
def restart():
    start_game()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=False)
