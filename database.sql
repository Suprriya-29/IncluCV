-- Connect to inclucv database first
\c inclucv;

-- Create Resumes table
CREATE TABLE IF NOT EXISTS Resumes (
    id                      SERIAL PRIMARY KEY,
    full_name               VARCHAR(100) NOT NULL,
    email                   VARCHAR(150) NOT NULL,
    phone                   VARCHAR(20),
    location                VARCHAR(100),
    disability_type         VARCHAR(100),
    comm_preference         VARCHAR(100),
    assistive_tools         VARCHAR(300),
    accommodation_requests  VARCHAR(500),
    summary                 VARCHAR(1000),
    skills                  VARCHAR(1000),
    experience              TEXT,
    education               TEXT,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create EmployerGuideTemplates table
CREATE TABLE IF NOT EXISTS EmployerGuideTemplates (
    id              SERIAL PRIMARY KEY,
    disability_type VARCHAR(100) NOT NULL,
    comm_preference VARCHAR(100) NOT NULL,
    guide_text      TEXT NOT NULL
);

-- Insert sample data
INSERT INTO EmployerGuideTemplates (disability_type, comm_preference, guide_text) VALUES
('Deaf', 'Sign Language', 'This guide has been auto-generated to help you work effectively with {name}.

COMMUNICATION:
- {name} communicates using Sign Language. Please arrange a certified interpreter for interviews and important meetings.
- For day-to-day communication, prefer written messages via email or chat tools like Microsoft Teams or Slack.
- Avoid phone calls — always use text-based alternatives.

INTERVIEWS:
- Conduct interviews via video call with an interpreter, or in person with an interpreter present.
- Share interview questions in writing in advance so {name} can prepare effectively.
- Allow extra time during interviews for interpretation.

WORKPLACE SETUP:
- Ensure visual alerts are available alongside audio alarms.
- Provide written meeting agendas and minutes for all meetings.
- Use captioning tools during video calls.

LEGAL NOTE:
Under the Rights of Persons with Disabilities Act 2016 (India), employers are required to make reasonable accommodations for employees with disabilities.'),

('Deaf', 'Text Chat', 'This guide has been auto-generated to help you work effectively with {name}.

COMMUNICATION:
- {name} prefers all communication in writing — use email, Teams chat, or Slack for everything.
- Avoid phone calls entirely. For urgent matters, send a text or chat message.
- During meetings, assign someone to type key points in real time.

INTERVIEWS:
- Conduct interviews via written chat, or video call with live captions enabled.
- Share all questions and documents in writing beforehand.

WORKPLACE SETUP:
- Set up visual desktop notifications for all alerts and messages.
- Use tools with strong captioning support.

LEGAL NOTE:
Under the Rights of Persons with Disabilities Act 2016 (India), reasonable workplace accommodations for deaf employees are legally required.'),

('Hard of Hearing', 'Lip Reading', 'This guide has been auto-generated to help you work effectively with {name}.

COMMUNICATION:
- {name} relies on lip reading. Always face {name} directly when speaking.
- Speak clearly and at a natural pace.
- Avoid covering your mouth or looking away while speaking.

INTERVIEWS:
- Conduct in a well-lit, quiet room. Ensure your face is clearly visible.
- Provide questions in writing as a backup.

WORKPLACE SETUP:
- Seat {name} where they can see speakers faces easily in meetings.
- Supplement verbal communication with written summaries after meetings.

LEGAL NOTE:
Under the Rights of Persons with Disabilities Act 2016 (India), employers must make reasonable accommodations.'),

('Mute', 'Text Chat', 'This guide has been auto-generated to help you work effectively with {name}.

COMMUNICATION:
- {name} does not use verbal speech. All communication should be in writing.
- Do not ask {name} to speak in meetings.
- {name} may use a text-to-speech app — be patient and allow time for responses.

INTERVIEWS:
- Conduct via written chat or allow {name} to type responses during interview.
- Avoid group verbal discussions without a text-based participation option.

WORKPLACE SETUP:
- Ensure {name} has a device and tools for text communication at all times.
- In team meetings, use a shared live document where everyone can type comments.

LEGAL NOTE:
Under the Rights of Persons with Disabilities Act 2016 (India), alternative communication methods are a legally recognised reasonable accommodation.');