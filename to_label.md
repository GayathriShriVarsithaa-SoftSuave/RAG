# Label these 25 answers BY HAND (do NOT run the judge first)

Rule: **PASS** = every factual statement in the ANSWER is supported by the EXCERPTS shown.
**FAIL** = at least one statement is not supported, is invented, or contradicts the excerpts.
An answer that starts with "REFUSE:" makes no claims, so label it PASS.

Write your labels in `labels_25.json` as "PASS" or "FAIL" for every id.

## Case 1
**Question:** Does this platform ingest raw vehicle CAN-bus or ECU data as part of its normal operation?

**Answer:** No, the platform does not ingest raw vehicle CAN-bus or ECU data as it is specifically excluded [chunk_id: NEURORA-PRD-v2.0.txt:naive:14, clause: None]. The PRD states that CAN-bus/ECU integration is outside the active scope [chunk_id: NEURORA-PRD-v2.0.txt:naive:16, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:14 | form_number: NEURORA-PRD v2.0 | clause: None
ot received the required approval.

## Exclusions Table

| Code | Description                                                           | Applies To (Excluded?)       |
| ---- | --------------------------------------------------------------------- | ---------------------------- |
| E-01 | Vehicle CAN-bus or ECU data ingestion and vehicle-control integration | Yes - excluded               |
| E-02 | Real-time safety intervention or collision avoidance                  | Yes - excluded               |
| E-03 | Autonomous driving or vehicle control                                 | Yes - excluded

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:13 | form_number: NEURORA-PRD v2.0 | clause: None
equires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data.

The platform also generates privacy-protected media derivatives by detecting and anonymising visible faces and vehicle registration plates. Original recordings are stored separately and are only accessible to authorised roles. Sharing and exporting can be blocked when required anonymisation processing has failed or has not received the required approval.

## Exclusions Table

| Code | Description

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:17 | form_number: NEURORA-PRD v2.0 | clause: None
ease lane detection are outside the active scope.

## Claims Note

Neurora is designed to transform raw multimodal training-session data into evidence-based behavioural insights and coaching feedback.

A key principle of the platform is that insights should remain explainable: trainers should be able to trace a finding back to the underlying session, clip, timestamp, AOI, metric, and processing version. Automated analysis can be reviewed and corrected by authorised users rather than being treated as unquestionable output.

In simple terms, the project follows this chain:

Capture → Synchronize

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

```

## Case 2
**Question:** Can the system step in to intervene and help a driver avoid a collision while it's happening?

**Answer:** No. Real-time safety intervention or collision avoidance is excluded from the system [chunk_id: NEURORA-PRD-v2.0.txt:naive:14, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:14 | form_number: NEURORA-PRD v2.0 | clause: None
ot received the required approval.

## Exclusions Table

| Code | Description                                                           | Applies To (Excluded?)       |
| ---- | --------------------------------------------------------------------- | ---------------------------- |
| E-01 | Vehicle CAN-bus or ECU data ingestion and vehicle-control integration | Yes - excluded               |
| E-02 | Real-time safety intervention or collision avoidance                  | Yes - excluded               |
| E-03 | Autonomous driving or vehicle control                                 | Yes - excluded

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:5 | form_number: NEURORA-PRD v2.0 | clause: None
ons, insights, comparisons, coaching recommendations, reports, and exports.

The system allows trainers to review processed clips, correct automatically detected Areas of Interest, examine gaze and physiological information, compare participants or sessions, and generate evidence-based coaching recommendations.

## Neurora Selfview

Neurora Selfview is the participant-facing application. It provides participants with controlled access to authorised sessions and clips, simplified performance summaries, trainer feedback, and approved recommendations.

It is intentionally not a raw-data analytics

```

## Case 3
**Question:** Is the platform able to drive the vehicle itself or take over vehicle control?

**Answer:** The platform excludes autonomous driving or vehicle control [chunk_id: NEURORA-PRD-v2.0.txt:naive:14, clause: None] and vehicle-control integration [chunk_id: NEURORA-PRD-v2.0.txt:naive:14, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:13 | form_number: NEURORA-PRD v2.0 | clause: None
equires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data.

The platform also generates privacy-protected media derivatives by detecting and anonymising visible faces and vehicle registration plates. Original recordings are stored separately and are only accessible to authorised roles. Sharing and exporting can be blocked when required anonymisation processing has failed or has not received the required approval.

## Exclusions Table

| Code | Description

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:14 | form_number: NEURORA-PRD v2.0 | clause: None
ot received the required approval.

## Exclusions Table

| Code | Description                                                           | Applies To (Excluded?)       |
| ---- | --------------------------------------------------------------------- | ---------------------------- |
| E-01 | Vehicle CAN-bus or ECU data ingestion and vehicle-control integration | Yes - excluded               |
| E-02 | Real-time safety intervention or collision avoidance                  | Yes - excluded               |
| E-03 | Autonomous driving or vehicle control                                 | Yes - excluded

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:10 | form_number: NEURORA-PRD v2.0 | clause: None
dic velocity, Total Eyes-Off-Road Time, heart rate, HRV, stress estimates, cognitive load, scan paths, heatmaps, and event-based measures.

The platform uses these measurements to generate insight categories such as:

* Hazard perception
* Visual strategy
* Distraction / eyes-off-road
* Cognitive tunnelling
* Fatigue indication
* Stress and workload
* Compliance and manoeuvre behaviour
* Participant progression
* Participant-to-participant comparison
* Expert-versus-novice comparison
* Voice-context correlation
* Study and condition comparison

## AI and Computer Vision

AI and computer vision

```

## Case 4
**Question:** Would a participant be able to get unrestricted, unsupervised access to someone else's raw biometric recordings?

**Answer:** No, participants do not have unrestricted access to raw biometric or raw recording data [chunk_id: NEURORA-PRD-v2.0.txt:naive:6, clause: None]. Unrestricted participant or public access to raw biometric data is explicitly excluded [chunk_id: NEURORA-PRD-v2.0.txt:naive:15, clause: None]. Furthermore, the platform utilizes role-based access control and tenant isolation, and original recordings are only accessible to authorised roles [chunk_id: NEURORA-PRD-v2.0.txt:naive:13, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:6 | form_number: NEURORA-PRD v2.0 | clause: None
ack, and approved recommendations.

It is intentionally not a raw-data analytics application. Participants only receive content that they are authorised to access, with the default experience being focused on selected clips and understandable feedback rather than unrestricted biometric or raw recording access.

## Shared Cloud Backend

The three products use a shared AWS-based backend responsible for identity, APIs, storage, event-driven processing, compute, model versioning, notifications, auditing, and administration.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:13 | form_number: NEURORA-PRD v2.0 | clause: None
equires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data.

The platform also generates privacy-protected media derivatives by detecting and anonymising visible faces and vehicle registration plates. Original recordings are stored separately and are only accessible to authorised roles. Sharing and exporting can be blocked when required anonymisation processing has failed or has not received the required approval.

## Exclusions Table

| Code | Description

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:5 | form_number: NEURORA-PRD v2.0 | clause: None
ons, insights, comparisons, coaching recommendations, reports, and exports.

The system allows trainers to review processed clips, correct automatically detected Areas of Interest, examine gaze and physiological information, compare participants or sessions, and generate evidence-based coaching recommendations.

## Neurora Selfview

Neurora Selfview is the participant-facing application. It provides participants with controlled access to authorised sessions and clips, simplified performance summaries, trainer feedback, and approved recommendations.

It is intentionally not a raw-data analytics

```

## Case 5
**Question:** Is lane detection or tracking a feature that is actively working right now in the shipped product?

**Answer:** No, lane detection or tracking is currently disabled [chunk_id: NEURORA-PRD-v2.0.txt:naive:15, clause: None]. It is explicitly listed as outside the active scope of the current product release [chunk_id: NEURORA-PRD-v2.0.txt:naive:16, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:17 | form_number: NEURORA-PRD v2.0 | clause: None
ease lane detection are outside the active scope.

## Claims Note

Neurora is designed to transform raw multimodal training-session data into evidence-based behavioural insights and coaching feedback.

A key principle of the platform is that insights should remain explainable: trainers should be able to trace a finding back to the underlying session, clip, timestamp, AOI, metric, and processing version. Automated analysis can be reviewed and corrected by authorised users rather than being treated as unquestionable output.

In simple terms, the project follows this chain:

Capture → Synchronize

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:11 | form_number: NEURORA-PRD v2.0 | clause: None
tudy and condition comparison

## AI and Computer Vision

AI and computer vision are used for Area of Interest detection, object tracking, gaze mapping, metric generation, and behavioural insights. Automated results are designed to remain explainable and reviewable by authorised trainers or analysts.

Every insight should be traceable back to the underlying metrics, timestamps, AOIs, data-quality information, and model or rule versions. AI outputs are intended as decision support for trainers rather than guaranteed statements about a person's intent, cognition, safety, or medical condition.

T

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:13 | form_number: NEURORA-PRD v2.0 | clause: None
equires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data.

The platform also generates privacy-protected media derivatives by detecting and anonymising visible faces and vehicle registration plates. Original recordings are stored separately and are only accessible to authorised roles. Sharing and exporting can be blocked when required anonymisation processing has failed or has not received the required approval.

## Exclusions Table

| Code | Description

```

## Case 6
**Question:** What devices does Neurora Capture integrate with to record eye-tracking and physiological data during a session?

**Answer:** Neurora Capture integrates with Pupil Labs Neon, Tobii Pro Glasses 3, Tobii Pro Glasses X, Polar H10, and the Soma Reality cognitive-load service [NEURORA-PRD-v2.0.txt:naive:3, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:3 | form_number: NEURORA-PRD v2.0 | clause: None
low.

## Neurora Capture

Neurora Capture is the trainer-operated mobile application responsible for the acquisition layer. It manages projects, participants, sessions, device connections, calibration, recording, event tagging, local storage, local replay, and cloud upload.

It integrates with supported devices such as Pupil Labs Neon, Tobii Pro Glasses 3, Tobii Pro Glasses X, Polar H10, and the Soma Reality cognitive-load service. During a session, the application can capture video, gaze, physiological data, cognitive-load data, GPS, optional audio, simulator events, and manual tags on a unif

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:7 | form_number: NEURORA-PRD v2.0 | clause: None
tion.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A trainer creates or selects a project, participant, and session and configures applicable study, protocol, scenario, devices, consent, GPS, and audio settings.
2. **Connect and Validate** — Capture connects the required devices, checks battery, signal, storage, consent, and calibration.
3. **Record** — Video, gaze, physiological, cognitive-load, GPS, audio, simulator events, and manual tags are captured using a unified timeline.
4. **Immediate Review** — The trainer can replay the recording locally with synchronize

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:4 | form_number: NEURORA-PRD v2.0 | clause: None
tive-load data, GPS, optional audio, simulator events, and manual tags on a unified timeline.

Capture also supports offline recording, encrypted local storage, reconnection handling, session recovery, local gaze-overlay replay, tagged-clip replay, and resumable multipart uploads.

## Neurora Insight

Neurora Insight is the central web-based experience for trainers, analysts, and supervisors. It provides session management, synchronized video playback, AOI detection and correction, metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports.

The

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:9 | form_number: NEURORA-PRD v2.0 | clause: None
icipants or sessions, create recommendations, and generate reports.
8. **Participant Feedback** — Selfview provides authorised clips, simplified summaries, trainer feedback, and controlled sharing to the participant.

## Data and Analysis

Neurora analyses eye-tracking, physiological, cognitive-load, and contextual information. Important metrics include fixation duration and count, fixation rate, time to first fixation, AOI dwell time, gaze entropy, road-centre gaze ratio, PERCLOS, blink rate, pupil dilation, saccadic velocity, Total Eyes-Off-Road Time, heart rate, HRV, stress estimates, cogni

```

## Case 7
**Question:** What can trainers and analysts do inside Neurora Insight with a recorded session?

**Answer:** Inside Neurora Insight, trainers and analysts can perform session management, synchronized video playback, AOI detection and correction, and access metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports [chunk_id: NEURORA-PRD-v2.0.txt:naive:4, clause: None]. Additionally, they can review processed clips, correct automatically detected Areas of Interest, examine gaze and physiological information, compare participants or sessions, and generate evidence-based coaching recommendations [chunk_id: NEURORA-PRD-v2.0.txt:naive:5, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:4 | form_number: NEURORA-PRD v2.0 | clause: None
tive-load data, GPS, optional audio, simulator events, and manual tags on a unified timeline.

Capture also supports offline recording, encrypted local storage, reconnection handling, session recovery, local gaze-overlay replay, tagged-clip replay, and resumable multipart uploads.

## Neurora Insight

Neurora Insight is the central web-based experience for trainers, analysts, and supervisors. It provides session management, synchronized video playback, AOI detection and correction, metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports.

The

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:2 | form_number: NEURORA-PRD v2.0 | clause: None
overall goal is to help trainers and analysts understand what a participant was looking at, what they may have missed, how their visual attention changed, and how physiological or cognitive-load changes relate to events during the training session. The resulting evidence can be converted into understandable coaching insights, recommendations, reports, and participant feedback.

## Product Components Overview

Neurora is made up of three products and a shared cloud backend, described individually in the sections below.

## Neurora Capture

Neurora Capture is the trainer-operated mobile applica

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:17 | form_number: NEURORA-PRD v2.0 | clause: None
ease lane detection are outside the active scope.

## Claims Note

Neurora is designed to transform raw multimodal training-session data into evidence-based behavioural insights and coaching feedback.

A key principle of the platform is that insights should remain explainable: trainers should be able to trace a finding back to the underlying session, clip, timestamp, AOI, metric, and processing version. Automated analysis can be reviewed and corrected by authorised users rather than being treated as unquestionable output.

In simple terms, the project follows this chain:

Capture → Synchronize

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:5 | form_number: NEURORA-PRD v2.0 | clause: None
ons, insights, comparisons, coaching recommendations, reports, and exports.

The system allows trainers to review processed clips, correct automatically detected Areas of Interest, examine gaze and physiological information, compare participants or sessions, and generate evidence-based coaching recommendations.

## Neurora Selfview

Neurora Selfview is the participant-facing application. It provides participants with controlled access to authorised sessions and clips, simplified performance summaries, trainer feedback, and approved recommendations.

It is intentionally not a raw-data analytics

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:7 | form_number: NEURORA-PRD v2.0 | clause: None
tion.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A trainer creates or selects a project, participant, and session and configures applicable study, protocol, scenario, devices, consent, GPS, and audio settings.
2. **Connect and Validate** — Capture connects the required devices, checks battery, signal, storage, consent, and calibration.
3. **Record** — Video, gaze, physiological, cognitive-load, GPS, audio, simulator events, and manual tags are captured using a unified timeline.
4. **Immediate Review** — The trainer can replay the recording locally with synchronize

```

## Case 8
**Question:** What kind of access does a participant get through Neurora Selfview, and is it a full raw-data analytics view?

**Answer:** Neurora Selfview provides participants with controlled access to authorised sessions and clips, simplified performance summaries, trainer feedback, and approved recommendations [chunk_id: NEURORA-PRD-v2.0.txt:naive:5, clause: None]. It is intentionally not a raw-data analytics application, and participants do not have unrestricted biometric or raw recording access [chunk_id: NEURORA-PRD-v2.0.txt:naive:6, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:5 | form_number: NEURORA-PRD v2.0 | clause: None
ons, insights, comparisons, coaching recommendations, reports, and exports.

The system allows trainers to review processed clips, correct automatically detected Areas of Interest, examine gaze and physiological information, compare participants or sessions, and generate evidence-based coaching recommendations.

## Neurora Selfview

Neurora Selfview is the participant-facing application. It provides participants with controlled access to authorised sessions and clips, simplified performance summaries, trainer feedback, and approved recommendations.

It is intentionally not a raw-data analytics

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:6 | form_number: NEURORA-PRD v2.0 | clause: None
ack, and approved recommendations.

It is intentionally not a raw-data analytics application. Participants only receive content that they are authorised to access, with the default experience being focused on selected clips and understandable feedback rather than unrestricted biometric or raw recording access.

## Shared Cloud Backend

The three products use a shared AWS-based backend responsible for identity, APIs, storage, event-driven processing, compute, model versioning, notifications, auditing, and administration.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:9 | form_number: NEURORA-PRD v2.0 | clause: None
icipants or sessions, create recommendations, and generate reports.
8. **Participant Feedback** — Selfview provides authorised clips, simplified summaries, trainer feedback, and controlled sharing to the participant.

## Data and Analysis

Neurora analyses eye-tracking, physiological, cognitive-load, and contextual information. Important metrics include fixation duration and count, fixation rate, time to first fixation, AOI dwell time, gaze entropy, road-centre gaze ratio, PERCLOS, blink rate, pupil dilation, saccadic velocity, Total Eyes-Off-Road Time, heart rate, HRV, stress estimates, cogni

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

```

## Case 9
**Question:** In the end-to-end Neurora workflow, what does a trainer do first, before any device is connected?

**Answer:** In the end-to-end Neurora workflow, the trainer first creates or selects a project, participant, and session, and then configures the applicable study, protocol, scenario, devices, consent, GPS, and audio settings [chunk_id: NEURORA-PRD-v2.0.txt:naive:7, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:7 | form_number: NEURORA-PRD v2.0 | clause: None
tion.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A trainer creates or selects a project, participant, and session and configures applicable study, protocol, scenario, devices, consent, GPS, and audio settings.
2. **Connect and Validate** — Capture connects the required devices, checks battery, signal, storage, consent, and calibration.
3. **Record** — Video, gaze, physiological, cognitive-load, GPS, audio, simulator events, and manual tags are captured using a unified timeline.
4. **Immediate Review** — The trainer can replay the recording locally with synchronize

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:6 | form_number: NEURORA-PRD v2.0 | clause: None
ack, and approved recommendations.

It is intentionally not a raw-data analytics application. Participants only receive content that they are authorised to access, with the default experience being focused on selected clips and understandable feedback rather than unrestricted biometric or raw recording access.

## Shared Cloud Backend

The three products use a shared AWS-based backend responsible for identity, APIs, storage, event-driven processing, compute, model versioning, notifications, auditing, and administration.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:3 | form_number: NEURORA-PRD v2.0 | clause: None
low.

## Neurora Capture

Neurora Capture is the trainer-operated mobile application responsible for the acquisition layer. It manages projects, participants, sessions, device connections, calibration, recording, event tagging, local storage, local replay, and cloud upload.

It integrates with supported devices such as Pupil Labs Neon, Tobii Pro Glasses 3, Tobii Pro Glasses X, Polar H10, and the Soma Reality cognitive-load service. During a session, the application can capture video, gaze, physiological data, cognitive-load data, GPS, optional audio, simulator events, and manual tags on a unif

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:17 | form_number: NEURORA-PRD v2.0 | clause: None
ease lane detection are outside the active scope.

## Claims Note

Neurora is designed to transform raw multimodal training-session data into evidence-based behavioural insights and coaching feedback.

A key principle of the platform is that insights should remain explainable: trainers should be able to trace a finding back to the underlying session, clip, timestamp, AOI, metric, and processing version. Automated analysis can be reviewed and corrected by authorised users rather than being treated as unquestionable output.

In simple terms, the project follows this chain:

Capture → Synchronize

```

## Case 10
**Question:** Which metric does Neurora use to measure how much time a driver's eyes spend off the road during a session?

**Answer:** Neurora uses the Total Eyes-Off-Road Time metric to measure eyes-off-road duration [chunk_id: NEURORA-PRD-v2.0.txt:naive:9, clause: None]; [chunk_id: NEURORA-PRD-v2.0.txt:naive:10, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:9 | form_number: NEURORA-PRD v2.0 | clause: None
icipants or sessions, create recommendations, and generate reports.
8. **Participant Feedback** — Selfview provides authorised clips, simplified summaries, trainer feedback, and controlled sharing to the participant.

## Data and Analysis

Neurora analyses eye-tracking, physiological, cognitive-load, and contextual information. Important metrics include fixation duration and count, fixation rate, time to first fixation, AOI dwell time, gaze entropy, road-centre gaze ratio, PERCLOS, blink rate, pupil dilation, saccadic velocity, Total Eyes-Off-Road Time, heart rate, HRV, stress estimates, cogni

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:10 | form_number: NEURORA-PRD v2.0 | clause: None
dic velocity, Total Eyes-Off-Road Time, heart rate, HRV, stress estimates, cognitive load, scan paths, heatmaps, and event-based measures.

The platform uses these measurements to generate insight categories such as:

* Hazard perception
* Visual strategy
* Distraction / eyes-off-road
* Cognitive tunnelling
* Fatigue indication
* Stress and workload
* Compliance and manoeuvre behaviour
* Participant progression
* Participant-to-participant comparison
* Expert-versus-novice comparison
* Voice-context correlation
* Study and condition comparison

## AI and Computer Vision

AI and computer vision

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:17 | form_number: NEURORA-PRD v2.0 | clause: None
ease lane detection are outside the active scope.

## Claims Note

Neurora is designed to transform raw multimodal training-session data into evidence-based behavioural insights and coaching feedback.

A key principle of the platform is that insights should remain explainable: trainers should be able to trace a finding back to the underlying session, clip, timestamp, AOI, metric, and processing version. Automated analysis can be reviewed and corrected by authorised users rather than being treated as unquestionable output.

In simple terms, the project follows this chain:

Capture → Synchronize

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:4 | form_number: NEURORA-PRD v2.0 | clause: None
tive-load data, GPS, optional audio, simulator events, and manual tags on a unified timeline.

Capture also supports offline recording, encrypted local storage, reconnection handling, session recovery, local gaze-overlay replay, tagged-clip replay, and resumable multipart uploads.

## Neurora Insight

Neurora Insight is the central web-based experience for trainers, analysts, and supervisors. It provides session management, synchronized video playback, AOI detection and correction, metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports.

The

```

## Case 11
**Question:** What access controls and security measures does the platform require for handling biometric data?

**Answer:** The platform requires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data [chunk_id: NEURORA-PRD-v2.0.txt:naive:13, clause: None]. Additionally, original recordings are stored separately and are only accessible to authorised roles [chunk_id: NEURORA-PRD-v2.0.txt:naive:13, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:13 | form_number: NEURORA-PRD v2.0 | clause: None
equires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data.

The platform also generates privacy-protected media derivatives by detecting and anonymising visible faces and vehicle registration plates. Original recordings are stored separately and are only accessible to authorised roles. Sharing and exporting can be blocked when required anonymisation processing has failed or has not received the required approval.

## Exclusions Table

| Code | Description

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:12 | form_number: NEURORA-PRD v2.0 | clause: None
statements about a person's intent, cognition, safety, or medical condition.

The platform also supports optional voice/think-aloud processing. Spoken content can be transcribed with word- or sentence-level timestamps and correlated with gaze, AOIs, physiology, cognitive load, and task events.

## Security and Privacy

Because Neurora handles sensitive behavioural, physiological, eye-tracking, video, audio, and potentially location data, the platform includes strong security and privacy requirements.

The system requires encryption in transit and at rest, secure key management, MFA, role-base

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:6 | form_number: NEURORA-PRD v2.0 | clause: None
ack, and approved recommendations.

It is intentionally not a raw-data analytics application. Participants only receive content that they are authorised to access, with the default experience being focused on selected clips and understandable feedback rather than unrestricted biometric or raw recording access.

## Shared Cloud Backend

The three products use a shared AWS-based backend responsible for identity, APIs, storage, event-driven processing, compute, model versioning, notifications, auditing, and administration.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

```

## Case 12
**Question:** According to the Claims Note, what should a trainer be able to trace an automated finding back to?

**Answer:** A trainer should be able to trace a finding back to the underlying session, clip, timestamp, AOI, metric, and processing version [chunk_id: NEURORA-PRD-v2.0.txt:naive:17, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:17 | form_number: NEURORA-PRD v2.0 | clause: None
ease lane detection are outside the active scope.

## Claims Note

Neurora is designed to transform raw multimodal training-session data into evidence-based behavioural insights and coaching feedback.

A key principle of the platform is that insights should remain explainable: trainers should be able to trace a finding back to the underlying session, clip, timestamp, AOI, metric, and processing version. Automated analysis can be reviewed and corrected by authorised users rather than being treated as unquestionable output.

In simple terms, the project follows this chain:

Capture → Synchronize

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:11 | form_number: NEURORA-PRD v2.0 | clause: None
tudy and condition comparison

## AI and Computer Vision

AI and computer vision are used for Area of Interest detection, object tracking, gaze mapping, metric generation, and behavioural insights. Automated results are designed to remain explainable and reviewable by authorised trainers or analysts.

Every insight should be traceable back to the underlying metrics, timestamps, AOIs, data-quality information, and model or rule versions. AI outputs are intended as decision support for trainers rather than guaranteed statements about a person's intent, cognition, safety, or medical condition.

T

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:5 | form_number: NEURORA-PRD v2.0 | clause: None
ons, insights, comparisons, coaching recommendations, reports, and exports.

The system allows trainers to review processed clips, correct automatically detected Areas of Interest, examine gaze and physiological information, compare participants or sessions, and generate evidence-based coaching recommendations.

## Neurora Selfview

Neurora Selfview is the participant-facing application. It provides participants with controlled access to authorised sessions and clips, simplified performance summaries, trainer feedback, and approved recommendations.

It is intentionally not a raw-data analytics

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:2 | form_number: NEURORA-PRD v2.0 | clause: None
overall goal is to help trainers and analysts understand what a participant was looking at, what they may have missed, how their visual attention changed, and how physiological or cognitive-load changes relate to events during the training session. The resulting evidence can be converted into understandable coaching insights, recommendations, reports, and participant feedback.

## Product Components Overview

Neurora is made up of three products and a shared cloud backend, described individually in the sections below.

## Neurora Capture

Neurora Capture is the trainer-operated mobile applica

```

## Case 14
**Question:** Does Neurora offer a mobile app for iOS and Android?

**Answer:** REFUSE: The indexed endorsements do not contain this information.

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:3 | form_number: NEURORA-PRD v2.0 | clause: None
low.

## Neurora Capture

Neurora Capture is the trainer-operated mobile application responsible for the acquisition layer. It manages projects, participants, sessions, device connections, calibration, recording, event tagging, local storage, local replay, and cloud upload.

It integrates with supported devices such as Pupil Labs Neon, Tobii Pro Glasses 3, Tobii Pro Glasses X, Polar H10, and the Soma Reality cognitive-load service. During a session, the application can capture video, gaze, physiological data, cognitive-load data, GPS, optional audio, simulator events, and manual tags on a unif

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:2 | form_number: NEURORA-PRD v2.0 | clause: None
overall goal is to help trainers and analysts understand what a participant was looking at, what they may have missed, how their visual attention changed, and how physiological or cognitive-load changes relate to events during the training session. The resulting evidence can be converted into understandable coaching insights, recommendations, reports, and participant feedback.

## Product Components Overview

Neurora is made up of three products and a shared cloud backend, described individually in the sections below.

## Neurora Capture

Neurora Capture is the trainer-operated mobile applica

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:12 | form_number: NEURORA-PRD v2.0 | clause: None
statements about a person's intent, cognition, safety, or medical condition.

The platform also supports optional voice/think-aloud processing. Spoken content can be transcribed with word- or sentence-level timestamps and correlated with gaze, AOIs, physiology, cognitive load, and task events.

## Security and Privacy

Because Neurora handles sensitive behavioural, physiological, eye-tracking, video, audio, and potentially location data, the platform includes strong security and privacy requirements.

The system requires encryption in transit and at rest, secure key management, MFA, role-base

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:4 | form_number: NEURORA-PRD v2.0 | clause: None
tive-load data, GPS, optional audio, simulator events, and manual tags on a unified timeline.

Capture also supports offline recording, encrypted local storage, reconnection handling, session recovery, local gaze-overlay replay, tagged-clip replay, and resumable multipart uploads.

## Neurora Insight

Neurora Insight is the central web-based experience for trainers, analysts, and supervisors. It provides session management, synchronized video playback, AOI detection and correction, metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports.

The

```

## Case 15
**Question:** What is the pricing for the enterprise tier of the Neurora platform?

**Answer:** REFUSE: The indexed endorsements do not contain this information.

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:0 | form_number: NEURORA-PRD v2.0 | clause: None
FORM_NUMBER: NEURORA-PRD v2.0
POLICY_LINE: Behavioral Intelligence Platform
EFFECTIVE_DATE: 2026-08-05
TITLE: AI-Powered Behavioral Intelligence and Training Analysis Platform
PROJECT_NAME: Neurora Behavioral Intelligence Platform
PRODUCTS: Neurora Capture | Neurora Insight | Neurora Selfview
DOCUMENT_VERSION: 2.0
PRIMARY_USE_CASE: Driver Training and Safety-Related Training

## Purpose

Neurora is an AI-powered behavioral intelligence platform designed to understand and evaluate human attention, workload, stress, and performance during real-world training activities, with an initial focus on

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:12 | form_number: NEURORA-PRD v2.0 | clause: None
statements about a person's intent, cognition, safety, or medical condition.

The platform also supports optional voice/think-aloud processing. Spoken content can be transcribed with word- or sentence-level timestamps and correlated with gaze, AOIs, physiology, cognitive load, and task events.

## Security and Privacy

Because Neurora handles sensitive behavioural, physiological, eye-tracking, video, audio, and potentially location data, the platform includes strong security and privacy requirements.

The system requires encryption in transit and at rest, secure key management, MFA, role-base

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:17 | form_number: NEURORA-PRD v2.0 | clause: None
ease lane detection are outside the active scope.

## Claims Note

Neurora is designed to transform raw multimodal training-session data into evidence-based behavioural insights and coaching feedback.

A key principle of the platform is that insights should remain explainable: trainers should be able to trace a finding back to the underlying session, clip, timestamp, AOI, metric, and processing version. Automated analysis can be reviewed and corrected by authorised users rather than being treated as unquestionable output.

In simple terms, the project follows this chain:

Capture → Synchronize

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:3 | form_number: NEURORA-PRD v2.0 | clause: None
low.

## Neurora Capture

Neurora Capture is the trainer-operated mobile application responsible for the acquisition layer. It manages projects, participants, sessions, device connections, calibration, recording, event tagging, local storage, local replay, and cloud upload.

It integrates with supported devices such as Pupil Labs Neon, Tobii Pro Glasses 3, Tobii Pro Glasses X, Polar H10, and the Soma Reality cognitive-load service. During a session, the application can capture video, gaze, physiological data, cognitive-load data, GPS, optional audio, simulator events, and manual tags on a unif

```

## Case 16
**Question:** Who is the CEO of the company that makes Neurora?

**Answer:** REFUSE: The indexed endorsements do not contain this information.

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:2 | form_number: NEURORA-PRD v2.0 | clause: None
overall goal is to help trainers and analysts understand what a participant was looking at, what they may have missed, how their visual attention changed, and how physiological or cognitive-load changes relate to events during the training session. The resulting evidence can be converted into understandable coaching insights, recommendations, reports, and participant feedback.

## Product Components Overview

Neurora is made up of three products and a shared cloud backend, described individually in the sections below.

## Neurora Capture

Neurora Capture is the trainer-operated mobile applica

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:0 | form_number: NEURORA-PRD v2.0 | clause: None
FORM_NUMBER: NEURORA-PRD v2.0
POLICY_LINE: Behavioral Intelligence Platform
EFFECTIVE_DATE: 2026-08-05
TITLE: AI-Powered Behavioral Intelligence and Training Analysis Platform
PROJECT_NAME: Neurora Behavioral Intelligence Platform
PRODUCTS: Neurora Capture | Neurora Insight | Neurora Selfview
DOCUMENT_VERSION: 2.0
PRIMARY_USE_CASE: Driver Training and Safety-Related Training

## Purpose

Neurora is an AI-powered behavioral intelligence platform designed to understand and evaluate human attention, workload, stress, and performance during real-world training activities, with an initial focus on

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:4 | form_number: NEURORA-PRD v2.0 | clause: None
tive-load data, GPS, optional audio, simulator events, and manual tags on a unified timeline.

Capture also supports offline recording, encrypted local storage, reconnection handling, session recovery, local gaze-overlay replay, tagged-clip replay, and resumable multipart uploads.

## Neurora Insight

Neurora Insight is the central web-based experience for trainers, analysts, and supervisors. It provides session management, synchronized video playback, AOI detection and correction, metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports.

The

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:3 | form_number: NEURORA-PRD v2.0 | clause: None
low.

## Neurora Capture

Neurora Capture is the trainer-operated mobile application responsible for the acquisition layer. It manages projects, participants, sessions, device connections, calibration, recording, event tagging, local storage, local replay, and cloud upload.

It integrates with supported devices such as Pupil Labs Neon, Tobii Pro Glasses 3, Tobii Pro Glasses X, Polar H10, and the Soma Reality cognitive-load service. During a session, the application can capture video, gaze, physiological data, cognitive-load data, GPS, optional audio, simulator events, and manual tags on a unif

```

## Case 18
**Question:** Does the platform support both autonomous driving and medical diagnosis features?

**Answer:** No, both autonomous driving and medical diagnosis features are excluded from the platform [chunk_id: NEURORA-PRD-v2.0.txt:naive:15, clause: None]. The product documentation explicitly states that autonomous driving or vehicle control and medical or clinical diagnosis are excluded [chunk_id: NEURORA-PRD-v2.0.txt:naive:15, clause: None] and are outside the active scope [chunk_id: NEURORA-PRD-v2.0.txt:naive:16, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:12 | form_number: NEURORA-PRD v2.0 | clause: None
statements about a person's intent, cognition, safety, or medical condition.

The platform also supports optional voice/think-aloud processing. Spoken content can be transcribed with word- or sentence-level timestamps and correlated with gaze, AOIs, physiology, cognitive load, and task events.

## Security and Privacy

Because Neurora handles sensitive behavioural, physiological, eye-tracking, video, audio, and potentially location data, the platform includes strong security and privacy requirements.

The system requires encryption in transit and at rest, secure key management, MFA, role-base

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:10 | form_number: NEURORA-PRD v2.0 | clause: None
dic velocity, Total Eyes-Off-Road Time, heart rate, HRV, stress estimates, cognitive load, scan paths, heatmaps, and event-based measures.

The platform uses these measurements to generate insight categories such as:

* Hazard perception
* Visual strategy
* Distraction / eyes-off-road
* Cognitive tunnelling
* Fatigue indication
* Stress and workload
* Compliance and manoeuvre behaviour
* Participant progression
* Participant-to-participant comparison
* Expert-versus-novice comparison
* Voice-context correlation
* Study and condition comparison

## AI and Computer Vision

AI and computer vision

```

## Case 19
**Question:** Is the biometric data encrypted, and who exactly is allowed to see it unencrypted?

**Answer:** The platform requires encryption for raw biometric data in transit and at rest [chunk_id: NEURORA-PRD-v2.0.txt:naive:13, clause: None]. Original recordings, which contain raw data, are only accessible to authorized roles [chunk_id: NEURORA-PRD-v2.0.txt:naive:13, clause: None]. Unrestricted participant or public access to raw biometric data is excluded [chunk_id: NEURORA-PRD-v2.0.txt:naive:15, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:13 | form_number: NEURORA-PRD v2.0 | clause: None
equires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data.

The platform also generates privacy-protected media derivatives by detecting and anonymising visible faces and vehicle registration plates. Original recordings are stored separately and are only accessible to authorised roles. Sharing and exporting can be blocked when required anonymisation processing has failed or has not received the required approval.

## Exclusions Table

| Code | Description

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:6 | form_number: NEURORA-PRD v2.0 | clause: None
ack, and approved recommendations.

It is intentionally not a raw-data analytics application. Participants only receive content that they are authorised to access, with the default experience being focused on selected clips and understandable feedback rather than unrestricted biometric or raw recording access.

## Shared Cloud Backend

The three products use a shared AWS-based backend responsible for identity, APIs, storage, event-driven processing, compute, model versioning, notifications, auditing, and administration.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:4 | form_number: NEURORA-PRD v2.0 | clause: None
tive-load data, GPS, optional audio, simulator events, and manual tags on a unified timeline.

Capture also supports offline recording, encrypted local storage, reconnection handling, session recovery, local gaze-overlay replay, tagged-clip replay, and resumable multipart uploads.

## Neurora Insight

Neurora Insight is the central web-based experience for trainers, analysts, and supervisors. It provides session management, synchronized video playback, AOI detection and correction, metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports.

The

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:12 | form_number: NEURORA-PRD v2.0 | clause: None
statements about a person's intent, cognition, safety, or medical condition.

The platform also supports optional voice/think-aloud processing. Spoken content can be transcribed with word- or sentence-level timestamps and correlated with gaze, AOIs, physiology, cognitive load, and task events.

## Security and Privacy

Because Neurora handles sensitive behavioural, physiological, eye-tracking, video, audio, and potentially location data, the platform includes strong security and privacy requirements.

The system requires encryption in transit and at rest, secure key management, MFA, role-base

```

## Case 20
**Question:** Can a participant both correct their own AOI tags and see other participants' sessions?

**Answer:** REFUSE: The indexed endorsements do not contain this information.

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:8 | form_number: NEURORA-PRD v2.0 | clause: None
mediate Review** — The trainer can replay the recording locally with synchronized gaze overlays and tagged clips without waiting for cloud processing.
5. **Upload and Process** — Session data is securely uploaded using resumable multipart transfers and processed through cloud pipelines.
6. **Analyse** — Insight displays synchronized video, AOIs, metrics, physiological/cognitive timelines, optional transcripts, and generated insights.
7. **Coach and Compare** — Trainers can correct AOIs, annotate clips, compare participants or sessions, create recommendations, and generate reports.
8. **Partici

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:9 | form_number: NEURORA-PRD v2.0 | clause: None
icipants or sessions, create recommendations, and generate reports.
8. **Participant Feedback** — Selfview provides authorised clips, simplified summaries, trainer feedback, and controlled sharing to the participant.

## Data and Analysis

Neurora analyses eye-tracking, physiological, cognitive-load, and contextual information. Important metrics include fixation duration and count, fixation rate, time to first fixation, AOI dwell time, gaze entropy, road-centre gaze ratio, PERCLOS, blink rate, pupil dilation, saccadic velocity, Total Eyes-Off-Road Time, heart rate, HRV, stress estimates, cogni

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:5 | form_number: NEURORA-PRD v2.0 | clause: None
ons, insights, comparisons, coaching recommendations, reports, and exports.

The system allows trainers to review processed clips, correct automatically detected Areas of Interest, examine gaze and physiological information, compare participants or sessions, and generate evidence-based coaching recommendations.

## Neurora Selfview

Neurora Selfview is the participant-facing application. It provides participants with controlled access to authorised sessions and clips, simplified performance summaries, trainer feedback, and approved recommendations.

It is intentionally not a raw-data analytics

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:4 | form_number: NEURORA-PRD v2.0 | clause: None
tive-load data, GPS, optional audio, simulator events, and manual tags on a unified timeline.

Capture also supports offline recording, encrypted local storage, reconnection handling, session recovery, local gaze-overlay replay, tagged-clip replay, and resumable multipart uploads.

## Neurora Insight

Neurora Insight is the central web-based experience for trainers, analysts, and supervisors. It provides session management, synchronized video playback, AOI detection and correction, metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports.

The

```

## Case 21
**Question:** wat divices does neurora capture intergrate with for eye tracking

**Answer:** Neurora Capture integrates with Pupil Labs Neon, Tobii Pro Glasses 3, and Tobii Pro Glasses X [chunk_id: NEURORA-PRD-v2.0.txt:naive:3, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:3 | form_number: NEURORA-PRD v2.0 | clause: None
low.

## Neurora Capture

Neurora Capture is the trainer-operated mobile application responsible for the acquisition layer. It manages projects, participants, sessions, device connections, calibration, recording, event tagging, local storage, local replay, and cloud upload.

It integrates with supported devices such as Pupil Labs Neon, Tobii Pro Glasses 3, Tobii Pro Glasses X, Polar H10, and the Soma Reality cognitive-load service. During a session, the application can capture video, gaze, physiological data, cognitive-load data, GPS, optional audio, simulator events, and manual tags on a unif

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:4 | form_number: NEURORA-PRD v2.0 | clause: None
tive-load data, GPS, optional audio, simulator events, and manual tags on a unified timeline.

Capture also supports offline recording, encrypted local storage, reconnection handling, session recovery, local gaze-overlay replay, tagged-clip replay, and resumable multipart uploads.

## Neurora Insight

Neurora Insight is the central web-based experience for trainers, analysts, and supervisors. It provides session management, synchronized video playback, AOI detection and correction, metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports.

The

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:12 | form_number: NEURORA-PRD v2.0 | clause: None
statements about a person's intent, cognition, safety, or medical condition.

The platform also supports optional voice/think-aloud processing. Spoken content can be transcribed with word- or sentence-level timestamps and correlated with gaze, AOIs, physiology, cognitive load, and task events.

## Security and Privacy

Because Neurora handles sensitive behavioural, physiological, eye-tracking, video, audio, and potentially location data, the platform includes strong security and privacy requirements.

The system requires encryption in transit and at rest, secure key management, MFA, role-base

```

## Case 22
**Question:** is lane detction curently enabled in teh product

**Answer:** Lane detection/tracking is currently disabled in the current product release [NEURORA-PRD-v2.0.txt:naive:15, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:17 | form_number: NEURORA-PRD v2.0 | clause: None
ease lane detection are outside the active scope.

## Claims Note

Neurora is designed to transform raw multimodal training-session data into evidence-based behavioural insights and coaching feedback.

A key principle of the platform is that insights should remain explainable: trainers should be able to trace a finding back to the underlying session, clip, timestamp, AOI, metric, and processing version. Automated analysis can be reviewed and corrected by authorised users rather than being treated as unquestionable output.

In simple terms, the project follows this chain:

Capture → Synchronize

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:4 | form_number: NEURORA-PRD v2.0 | clause: None
tive-load data, GPS, optional audio, simulator events, and manual tags on a unified timeline.

Capture also supports offline recording, encrypted local storage, reconnection handling, session recovery, local gaze-overlay replay, tagged-clip replay, and resumable multipart uploads.

## Neurora Insight

Neurora Insight is the central web-based experience for trainers, analysts, and supervisors. It provides session management, synchronized video playback, AOI detection and correction, metrics, visualisations, annotations, insights, comparisons, coaching recommendations, reports, and exports.

The

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:14 | form_number: NEURORA-PRD v2.0 | clause: None
ot received the required approval.

## Exclusions Table

| Code | Description                                                           | Applies To (Excluded?)       |
| ---- | --------------------------------------------------------------------- | ---------------------------- |
| E-01 | Vehicle CAN-bus or ECU data ingestion and vehicle-control integration | Yes - excluded               |
| E-02 | Real-time safety intervention or collision avoidance                  | Yes - excluded               |
| E-03 | Autonomous driving or vehicle control                                 | Yes - excluded

```

## Case 23
**Question:** can this thing drive the car by itself lol

**Answer:** No, the platform does not provide autonomous driving or vehicle control, as these functions are excluded [chunk_id: NEURORA-PRD-v2.0.txt:naive:14, clause: None], [chunk_id: NEURORA-PRD-v2.0.txt:naive:15, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:14 | form_number: NEURORA-PRD v2.0 | clause: None
ot received the required approval.

## Exclusions Table

| Code | Description                                                           | Applies To (Excluded?)       |
| ---- | --------------------------------------------------------------------- | ---------------------------- |
| E-01 | Vehicle CAN-bus or ECU data ingestion and vehicle-control integration | Yes - excluded               |
| E-02 | Real-time safety intervention or collision avoidance                  | Yes - excluded               |
| E-03 | Autonomous driving or vehicle control                                 | Yes - excluded

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:12 | form_number: NEURORA-PRD v2.0 | clause: None
statements about a person's intent, cognition, safety, or medical condition.

The platform also supports optional voice/think-aloud processing. Spoken content can be transcribed with word- or sentence-level timestamps and correlated with gaze, AOIs, physiology, cognitive load, and task events.

## Security and Privacy

Because Neurora handles sensitive behavioural, physiological, eye-tracking, video, audio, and potentially location data, the platform includes strong security and privacy requirements.

The system requires encryption in transit and at rest, secure key management, MFA, role-base

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:5 | form_number: NEURORA-PRD v2.0 | clause: None
ons, insights, comparisons, coaching recommendations, reports, and exports.

The system allows trainers to review processed clips, correct automatically detected Areas of Interest, examine gaze and physiological information, compare participants or sessions, and generate evidence-based coaching recommendations.

## Neurora Selfview

Neurora Selfview is the participant-facing application. It provides participants with controlled access to authorised sessions and clips, simplified performance summaries, trainer feedback, and approved recommendations.

It is intentionally not a raw-data analytics

```

## Case 24
**Question:** What form number and version does this PRD document carry?

**Answer:** The PRD document carries form number NEURORA-PRD v2.0 [chunk_id: NEURORA-PRD-v2.0.txt:naive:0, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:0 | form_number: NEURORA-PRD v2.0 | clause: None
FORM_NUMBER: NEURORA-PRD v2.0
POLICY_LINE: Behavioral Intelligence Platform
EFFECTIVE_DATE: 2026-08-05
TITLE: AI-Powered Behavioral Intelligence and Training Analysis Platform
PROJECT_NAME: Neurora Behavioral Intelligence Platform
PRODUCTS: Neurora Capture | Neurora Insight | Neurora Selfview
DOCUMENT_VERSION: 2.0
PRIMARY_USE_CASE: Driver Training and Safety-Related Training

## Purpose

Neurora is an AI-powered behavioral intelligence platform designed to understand and evaluate human attention, workload, stress, and performance during real-world training activities, with an initial focus on

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:13 | form_number: NEURORA-PRD v2.0 | clause: None
equires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data.

The platform also generates privacy-protected media derivatives by detecting and anonymising visible faces and vehicle registration plates. Original recordings are stored separately and are only accessible to authorised roles. Sharing and exporting can be blocked when required anonymisation processing has failed or has not received the required approval.

## Exclusions Table

| Code | Description

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:11 | form_number: NEURORA-PRD v2.0 | clause: None
tudy and condition comparison

## AI and Computer Vision

AI and computer vision are used for Area of Interest detection, object tracking, gaze mapping, metric generation, and behavioural insights. Automated results are designed to remain explainable and reviewable by authorised trainers or analysts.

Every insight should be traceable back to the underlying metrics, timestamps, AOIs, data-quality information, and model or rule versions. AI outputs are intended as decision support for trainers rather than guaranteed statements about a person's intent, cognition, safety, or medical condition.

T

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:6 | form_number: NEURORA-PRD v2.0 | clause: None
ack, and approved recommendations.

It is intentionally not a raw-data analytics application. Participants only receive content that they are authorised to access, with the default experience being focused on selected clips and understandable feedback rather than unrestricted biometric or raw recording access.

## Shared Cloud Backend

The three products use a shared AWS-based backend responsible for identity, APIs, storage, event-driven processing, compute, model versioning, notifications, auditing, and administration.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A

```

## Case 25
**Question:** How many exclusion codes are listed in the Exclusions Table?

**Answer:** There are 8 exclusion codes listed in the Exclusions Table (E-01 through E-08) [chunk_id: NEURORA-PRD-v2.0.txt:naive:14, clause: None], [chunk_id: NEURORA-PRD-v2.0.txt:naive:15, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:14 | form_number: NEURORA-PRD v2.0 | clause: None
ot received the required approval.

## Exclusions Table

| Code | Description                                                           | Applies To (Excluded?)       |
| ---- | --------------------------------------------------------------------- | ---------------------------- |
| E-01 | Vehicle CAN-bus or ECU data ingestion and vehicle-control integration | Yes - excluded               |
| E-02 | Real-time safety intervention or collision avoidance                  | Yes - excluded               |
| E-03 | Autonomous driving or vehicle control                                 | Yes - excluded

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:13 | form_number: NEURORA-PRD v2.0 | clause: None
equires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data.

The platform also generates privacy-protected media derivatives by detecting and anonymising visible faces and vehicle registration plates. Original recordings are stored separately and are only accessible to authorised roles. Sharing and exporting can be blocked when required anonymisation processing has failed or has not received the required approval.

## Exclusions Table

| Code | Description

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:3 | form_number: NEURORA-PRD v2.0 | clause: None
low.

## Neurora Capture

Neurora Capture is the trainer-operated mobile application responsible for the acquisition layer. It manages projects, participants, sessions, device connections, calibration, recording, event tagging, local storage, local replay, and cloud upload.

It integrates with supported devices such as Pupil Labs Neon, Tobii Pro Glasses 3, Tobii Pro Glasses X, Polar H10, and the Soma Reality cognitive-load service. During a session, the application can capture video, gaze, physiological data, cognitive-load data, GPS, optional audio, simulator events, and manual tags on a unif

```

## Case 26
**Question:** Is real-time collision intervention something this platform actually does?

**Answer:** No, real-time safety intervention or collision avoidance is excluded from the platform [chunk_id: NEURORA-PRD-v2.0.txt:naive:14, clause: None]. Furthermore, the PRD specifically states that real-time safety intervention is outside the active scope [chunk_id: NEURORA-PRD-v2.0.txt:naive:16, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:14 | form_number: NEURORA-PRD v2.0 | clause: None
ot received the required approval.

## Exclusions Table

| Code | Description                                                           | Applies To (Excluded?)       |
| ---- | --------------------------------------------------------------------- | ---------------------------- |
| E-01 | Vehicle CAN-bus or ECU data ingestion and vehicle-control integration | Yes - excluded               |
| E-02 | Real-time safety intervention or collision avoidance                  | Yes - excluded               |
| E-03 | Autonomous driving or vehicle control                                 | Yes - excluded

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:1 | form_number: NEURORA-PRD v2.0 | clause: None
and performance during real-world training activities, with an initial focus on driver training and safety-related training.

The platform combines multiple sources of synchronized data, including first-person video, eye-tracking/gaze data, physiological data, cognitive-load data, GPS, and optional audio or think-aloud narration. Instead of relying only on instructor observation and post-session recall, Neurora provides a single workflow for capturing, processing, analysing, and reviewing this multimodal data.

The overall goal is to help trainers and analysts understand what a participant was

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:10 | form_number: NEURORA-PRD v2.0 | clause: None
dic velocity, Total Eyes-Off-Road Time, heart rate, HRV, stress estimates, cognitive load, scan paths, heatmaps, and event-based measures.

The platform uses these measurements to generate insight categories such as:

* Hazard perception
* Visual strategy
* Distraction / eyes-off-road
* Cognitive tunnelling
* Fatigue indication
* Stress and workload
* Compliance and manoeuvre behaviour
* Participant progression
* Participant-to-participant comparison
* Expert-versus-novice comparison
* Voice-context correlation
* Study and condition comparison

## AI and Computer Vision

AI and computer vision

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:12 | form_number: NEURORA-PRD v2.0 | clause: None
statements about a person's intent, cognition, safety, or medical condition.

The platform also supports optional voice/think-aloud processing. Spoken content can be transcribed with word- or sentence-level timestamps and correlated with gaze, AOIs, physiology, cognitive load, and task events.

## Security and Privacy

Because Neurora handles sensitive behavioural, physiological, eye-tracking, video, audio, and potentially location data, the platform includes strong security and privacy requirements.

The system requires encryption in transit and at rest, secure key management, MFA, role-base

```

## Case 27
**Question:** If two participants are in the same session, can one see the other's raw biometric feed without permission?

**Answer:** Participants only receive content that they are authorised to access [chunk_id: NEURORA-PRD-v2.0.txt:naive:6, clause: None]. Unrestricted participant or public access to raw biometric data is excluded from the platform [chunk_id: NEURORA-PRD-v2.0.txt:naive:15, clause: None], and original recordings are only accessible to authorised roles [chunk_id: NEURORA-PRD-v2.0.txt:naive:13, clause: None].

Excerpts the assistant was given:
```
chunk_id: NEURORA-PRD-v2.0.txt:naive:6 | form_number: NEURORA-PRD v2.0 | clause: None
ack, and approved recommendations.

It is intentionally not a raw-data analytics application. Participants only receive content that they are authorised to access, with the default experience being focused on selected clips and understandable feedback rather than unrestricted biometric or raw recording access.

## Shared Cloud Backend

The three products use a shared AWS-based backend responsible for identity, APIs, storage, event-driven processing, compute, model versioning, notifications, auditing, and administration.

## End-to-End Workflow

The typical Neurora workflow is:

1. **Plan** — A

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:13 | form_number: NEURORA-PRD v2.0 | clause: None
equires encryption in transit and at rest, secure key management, MFA, role-based access control, tenant isolation, signed media access, audit logging, and controlled access to raw biometric data.

The platform also generates privacy-protected media derivatives by detecting and anonymising visible faces and vehicle registration plates. Original recordings are stored separately and are only accessible to authorised roles. Sharing and exporting can be blocked when required anonymisation processing has failed or has not received the required approval.

## Exclusions Table

| Code | Description

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:15 | form_number: NEURORA-PRD v2.0 | clause: None
mous driving or vehicle control                                 | Yes - excluded               |
| E-04 | Medical or clinical diagnosis                                         | Yes - excluded               |
| E-05 | Large-scale custom AI model training unless separately commissioned   | Yes - excluded               |
| E-06 | Unrestricted participant/public access to raw biometric data          | Yes - excluded               |
| E-07 | Lane detection/tracking in the current product release                | Yes - currently disabled     |
| E-08 | Eye tracking, video, physiological and cogniti

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:16 | form_number: NEURORA-PRD v2.0 | clause: None
currently disabled     |
| E-08 | Eye tracking, video, physiological and cognitive-load analysis        | No - core functionality      |
| E-09 | Trainer review, AOI correction and coaching recommendations           | No - core functionality      |
| E-10 | Participant feedback through Neurora Selfview                         | No - supported functionality |

The PRD specifically states that CAN-bus/ECU integration, real-time safety intervention, medical diagnosis, unrestricted raw biometric access, and current-release lane detection are outside the active scope.

## Claims Note

Neurora is de

---
chunk_id: NEURORA-PRD-v2.0.txt:naive:5 | form_number: NEURORA-PRD v2.0 | clause: None
ons, insights, comparisons, coaching recommendations, reports, and exports.

The system allows trainers to review processed clips, correct automatically detected Areas of Interest, examine gaze and physiological information, compare participants or sessions, and generate evidence-based coaching recommendations.

## Neurora Selfview

Neurora Selfview is the participant-facing application. It provides participants with controlled access to authorised sessions and clips, simplified performance summaries, trainer feedback, and approved recommendations.

It is intentionally not a raw-data analytics

```
