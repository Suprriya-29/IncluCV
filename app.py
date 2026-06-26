# ============================================================
#  IncluCV - Flask Backend (PostgreSQL version)
#  File: app.py
#  Run with: python app.py
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import json

app = Flask(__name__)
app.secret_key = "inclucv_secret_key_2024"

# ── Database connection ──────────────────────────────────────
def get_db_connection():
  def get_db_connection():
    try:
        conn = psycopg2.connect(
            "postgresql://inclucv_user:hHpLdpfQJP5RBJvuJBPLJcypFk6XteuN@dpg-d8v5r38js32c738navig-a.oregon-postgres.render.com/inclucv?sslmode=require"
        )
        return conn
    except Exception as e:
        print(f"Connection error: {e}")
        return None
    


# ── Home page ────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── Resume Builder ───────────────────────────────────────────
@app.route("/builder", methods=["GET", "POST"])
def builder():
    if request.method == "GET":
        return render_template("builder.html")

    full_name   = request.form.get("full_name", "").strip()
    email       = request.form.get("email", "").strip()
    phone       = request.form.get("phone", "").strip()
    location    = request.form.get("location", "").strip()

    disability_type        = request.form.get("disability_type", "").strip()
    comm_preference        = request.form.get("comm_preference", "").strip()
    assistive_tools        = request.form.get("assistive_tools", "").strip()
    accommodation_requests = request.form.get("accommodation_requests", "").strip()

    summary = request.form.get("summary", "").strip()
    skills  = request.form.get("skills", "").strip()

    exp_titles    = request.form.getlist("exp_title")
    exp_companies = request.form.getlist("exp_company")
    exp_years     = request.form.getlist("exp_years")
    exp_descs     = request.form.getlist("exp_desc")

    experience = []
    for i in range(len(exp_titles)):
        if exp_titles[i].strip():
            experience.append({
                "title":   exp_titles[i].strip(),
                "company": exp_companies[i].strip() if i < len(exp_companies) else "",
                "years":   exp_years[i].strip()     if i < len(exp_years)     else "",
                "desc":    exp_descs[i].strip()      if i < len(exp_descs)     else "",
            })

    edu_degrees = request.form.getlist("edu_degree")
    edu_schools = request.form.getlist("edu_school")
    edu_years   = request.form.getlist("edu_year")

    education = []
    for i in range(len(edu_degrees)):
        if edu_degrees[i].strip():
            education.append({
                "degree": edu_degrees[i].strip(),
                "school": edu_schools[i].strip() if i < len(edu_schools) else "",
                "year":   edu_years[i].strip()   if i < len(edu_years)   else "",
            })

    # ── Save to database ─────────────────────────────────────
    try:
        conn   = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO resumes (
                full_name, email, phone, location,
                disability_type, comm_preference, assistive_tools, accommodation_requests,
                summary, skills, experience, education
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            full_name, email, phone, location,
            disability_type, comm_preference, assistive_tools, accommodation_requests,
            summary, skills,
            json.dumps(experience),
            json.dumps(education)
        ))

        resume_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

    except Exception as e:
        return f"<h2>Database error: {e}</h2><p>Check your PostgreSQL connection in app.py</p>"

    # ── Generate employer guide ───────────────────────────────
    employer_guide = generate_employer_guide(
        full_name, disability_type, comm_preference
    )

    session["resume"] = {
        "id":             resume_id,
        "full_name":      full_name,
        "email":          email,
        "phone":          phone,
        "location":       location,
        "disability_type":        disability_type,
        "comm_preference":        comm_preference,
        "assistive_tools":        assistive_tools,
        "accommodation_requests": accommodation_requests,
        "summary":    summary,
        "skills":     skills,
        "experience": experience,
        "education":  education,
    }
    session["employer_guide"] = employer_guide

    return redirect(url_for("result"))


# ── Result page ───────────────────────────────────────────────
@app.route("/result")
def result():
    resume         = session.get("resume")
    employer_guide = session.get("employer_guide")

    if not resume:
        return redirect(url_for("builder"))

    skills_list = [s.strip() for s in resume["skills"].split(",") if s.strip()]

    return render_template(
        "result.html",
        resume=resume,
        skills_list=skills_list,
        employer_guide=employer_guide
    )


# ── Generate employer guide ───────────────────────────────────
def generate_employer_guide(name, disability_type, comm_preference):
    try:
        conn   = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT guide_text FROM employerguidetemplates
            WHERE disability_type = %s AND comm_preference = %s
        """, (disability_type, comm_preference))

        row = cursor.fetchone()

        if not row:
            cursor.execute("""
                SELECT guide_text FROM employerguidetemplates
                WHERE disability_type = %s LIMIT 1
            """, (disability_type,))
            row = cursor.fetchone()

        conn.close()

        if row:
            return row[0].replace("{name}", name)

    except Exception:
        pass

    return f"""This guide has been auto-generated to help you work effectively with {name}.

COMMUNICATION:
- Please discuss with {name} their preferred communication method before the first day.
- Always provide written versions of important verbal communications.
- Be patient and flexible — communication preferences may vary by situation.

INTERVIEWS:
- Ask {name} in advance what format works best for them.
- Provide questions in writing where possible.

WORKPLACE SETUP:
- Conduct an accessibility review of the workspace before {name} joins.
- Assign a buddy or point of contact for the first few weeks.

LEGAL NOTE:
Under the Rights of Persons with Disabilities Act 2016 (India), employers are legally required to make reasonable accommodations for employees with disabilities."""


# ── Run the app ───────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)