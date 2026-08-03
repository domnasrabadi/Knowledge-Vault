---
type: article
status: structured
quality:
topics: [llm-risks]
source: ""
created: 2025-06-01
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- hazard as a potential source of harm caused by the behavioral malfunction of an item regarding its intended design
- AI hazards vary significantly across manifold dimensions, such as the life cycle phase in which they emerge, the system components they impact, and the stakeholders they involve. To ensure systematic management of these AI hazards, we propose a taxonomy that characterizes them based on diverse attributes. This taxonomy subsequently provides an indication of the optimal methods for the detection, evaluation, and mitigation of a specific AI hazard, as well as the responsible parties for executing these actions

![[Screenshot 2025-06-01 at 7.45.07 pm.png]]


- AI hazards may materialize during various phases of an AI system’s life cycle. For instance, issues triggered by bias in training data emerge during the data collection and preparation stages. On the other hand, data drift serves as an example of an AI hazard that arises during the AI system’s operation. Additionally, certain AI hazards may span multiple phases of the AI system

# 1 The List
- **AIH 1: Inadequate specification of ODD**  
    The operational design domain (ODD) is a technical description of the application’s operational environment, initially conceptualized for autonomous driving systems. An inadequate specification of the ODD limits essential functions such as testing the learned functionality and out-of-distribution detection.
    
- **AIH 2: Inappropriate degree of automation**  
    The AI application’s degree of automation ranges from no automation to fully autonomous. AI applications with a high degree of automation may exhibit unexpected behaviour and pose risks in terms of their reliability and safety.
    
- **AIH 3: Inadequate planning of performance requirements**  
    The expected performance of the AI system should be planned adequately. An important aspect is that chosen performance metrics are meaningful for presenting the intended functionality. Otherwise, expectations and safety requirements can be unfulfillable at later life-cycle stages.
    
- **AIH 4: Insufficient AI development documentation**  
    Throughout the development of an AI system, it is vital to document every decision and action taken. This is not only essential to optimize the development process itself but also required for the auditability of the AI system.
    
- **AIH 5: Inappropriate degree of transparency to end users**  
    Transparency to end users of the AI system increases the user’s trust in the AI application. If transparency is not adequately integrated into the design, this might prevent the proper operation and cause potential misuse of the AI application.
    
- **AIH 6: Missing requirements for the implemented hardware**  
    The development and operation of an AI system can require significant amounts of computational power. If hardware selection does not consider these requirements, issues can arise during both development and deployment.
    
- **AIH 7: Choice of untrustworthy data source**  
    Choosing a trustworthy data source is a first prerequisite in order to fulfill data quality requirements. This is especially the case if third-party data sources are used to develop the AI system.
    
- **AIH 8: Lack of data understanding**  
    The correct understanding of the data used for developing an AI system is a prerequisite to avoid data shortcomings and hinders the development of an AI system which best suits the intended functionality.
    
- **AIH 9: Discriminative data bias**  
    Discriminative data bias describes the systematic discrimination of groups of persons in the form of data shortcomings, such as distributional representation or incorrectness. Data bias can manifest in the model and lead to unfair decisions if not appropriately treated.
    
- **AIH 10: Harming users’ data privacy**  
    Modern AI systems rely on large amounts of data. If this includes personal data about individuals, the risk of harming the privacy of persons arises.
    
- **AIH 11: Incorrect data labels**  
    Data labels are essential for any supervised learning algorithm since they preset the result of the learning process. If the correctness of the data labels is not given, the AI system is prevented from learning the ground truth and therefore the intended functionality.
    
- **AIH 12: Data poisoning**  
    Data poisoning describes an attack in the form of an injection of malicious data into the training set. If not prevented, this attack leads the AI system to learn unintended behavior.
    
- **AIH 13: Insufficient data representation**  
    The distribution of the data used for training a model should match the operational data’s distribution while consisting of sufficiently many samples. An important aspect of matching distributions between training and operational data is that also data which is rarely confronting the AI system in operation is represented in the training data.
    
- **AIH 14: Problems of synthetic data**  
    In the case of sparse data quantity, the simulation or generation of data is a valid alternative. However, it is essential to make sure that the simulated data is sufficiently similar to real data, especially in the way the AI system perceives them. Otherwise, generalization to operational data and reliable operational behavior cannot be guaranteed.
    
- **AIH 15: Inappropriate data splitting**  
    In data-driven AI development, the annotated data set is commonly split into training, validation, and test sets, whereby it is essential that the test set is not used for development but only for evaluation. Using the test set for training manipulates the testing strategy, which is the basis of the system’s quality assurance.
    
- **AIH 16: Poor model design choices**  
    The model specifications have significant impact on the functionality of an AI system. A developer making wrong decisions might cause the AI system to behave in a biased and unreliable manner.
    
- **AIH 17: Over- and underfitting**  
    Over- and underfitting describe the over- or insufficient adaptation of a model to training data. Both phenomena can cause an AI system to behave unreliably when confronted with operational data.
    
- **AIH 18: Lack of explainability**  
    The explainability of AI systems based on so-called black-box models is often limited. This opaqueness of AI systems can prevent developers from detecting shortcomings in the data or the model itself and decrease the performance and safety levels of the AI system.
    
- **AIH 19: Unreliability in corner cases**  
    AI systems tend to show unreliable behavior when confronted with rare or ambiguous input data, also called corner cases. Therefore, controlled behavior is required whenever the AI system faces a corner case.
    
- **AIH 20: Lack of robustness**  
    Robustness characterizes the resilience of an AI system’s output against minor changes in the input domain. A great variation in an AI system’s response to small input changes indicates unreliable outputs.
    
- **AIH 21: Uncertainty concerns**  
    AI systems should be able not only to return output for a given instance but also to provide a corresponding level of confidence. If such a method is not implemented or not working correctly, this can have a negative impact on performance and safety.
    
- **AIH 22: Operational data issues**  
    Until the deployment of the AI application into its operational environment, the AI system has been tested with a test set that aims to approximate the distribution of operational data. However, an unexpected deviation in this approximation can cause an AI application to behave unreliably. Therefore, its behavior under confrontation with operational data needs to be evaluated.
    
- **AIH 23: Data drift**  
    Data drift is a phenomenon in which the distribution of operational input data departs from those used during training. This can cause a degradation in performance.

# 2 Case Study
In this case study, the authors apply the AI Hazard Management (AIHM) framework to a protective solution designed for distribution power grids. The core challenge is detecting residual currents caused by high-impedance ground faults (HIGFs). Unlike low‐impedance faults, HIGFs allow only tiny leakage currents to flow to ground, making them extremely difficult to spot with traditional protection relays. Yet undetected HIGFs can over time cause vegetation to ignite or equipment to fail, potentially triggering wildfires or equipment damage.

To address this, the team proposes a decision‐support tool based on a deep neural network (DNN) classifier. The model’s input consists of time‐series measurements of voltage and current from one or more distribution feeders; its output is a simple “yes/no” decision as to whether a HIGF is present. Currently, the AI system is not intended to actuate control devices directly; instead, if the DNN outputs a positive HIGF detection, an alert is sent to human operators, who then verify and decide on any corrective action (e.g., inspecting a line segment, de‐energizing equipment, or clearing vegetation).

To simulate how the AIHM framework would guide risk management in practice, the authors conducted a structured, multi‐session interview with the lead data scientist and domain expert. Over four hours (divided into three sessions), they walked through each AIHM decision point—identification, assessment, mitigation, and documentation—focusing specifically on four hazards that span different lifecycle stages: discriminative data bias, lack of robustness, inappropriate transparency to end users, and data drift. In each case, they started by determining whether the hazard applied to this particular HIGF‐detection scenario; if it did, they devised acceptance criteria and mitigation steps, then wrapped up by specifying how everything would be recorded in the project’s audit trail.

1. **Discriminative Data Bias**
    - **Context:** Since the DNN’s training data consists exclusively of simulated or measured voltage and current waveforms (rather than demographic or socioeconomic attributes), there is no obvious way for representation bias to creep in (e.g., underrepresentation of “groups” of data). In other words, all training examples are drawn from the same distribution of physical sensor readings.
    - **Outcome:** After a brief discussion, the team concluded that discriminative data bias was not relevant: there are no “subpopulations” of sensors or customers whose data might be systematically under- or overrepresented. As a result, they marked this hazard as “irrelevant” in AIHM’s filtering step and documented that finding, so future auditors can see why no further action was needed.
2. **Lack of Robustness**
    - **Context:** Even though adversarial hacking of power‐grid sensors is deemed implausible (an attacker would have to inject precisely crafted signals into live feeders), there is still a real risk that normal measurement noise, sensor drift, or communication glitches could perturb the DNN’s inputs. If those perturbations cause the model to misclassify a genuine HIGF as safe, the system could fail to alert operators to a dangerous condition.
    - **Assessment:** The team selected a set of “meaningful perturbations” to simulate scenarios such as random voltage spikes, missing samples, or slight timing shifts. They then defined an acceptance threshold: for instance, the DNN’s detection‐accuracy drop on these perturbed inputs must not exceed 5% relative to its baseline performance on clean data.
    - **Mitigation:** If the unmitigated model failed to meet this threshold, they would retrain the DNN on an augmented dataset that includes those perturbations (e.g., adding Gaussian noise, simulating missing‐data patterns, or injecting synthetic transients). After retraining, they’d re‐evaluate accuracy on both clean and perturbed data to confirm that the robustness improvement did not degrade baseline performance by more than, say, 2% (balancing the known robustness‐accuracy trade‐off).
    - **Documentation:** Every choice—selection of perturbation types, the numeric performance thresholds, the specific augmentation method (e.g., “5 ms jitter added to voltage waveforms with standard deviation 0.5 V”), and all pre‐ and post‐retraining evaluation metrics—was recorded in a “robustness audit log.”
3. **Inappropriate Degree of Transparency to End Users**
    - **Context:** The DNN is fundamentally a “black box,” meaning that operators cannot directly see why it flagged or cleared a suspected HIGF. However, because a false positive might lead to an unnecessary shutdown of a feeder or a false negative might let a dangerous condition go unaddressed, the team decided that operators need more insight into the model’s reasoning.
    - **Assessment:** Rather than attempt to assign a numerical “transparency score,” they conducted a qualitative exercise: they sketched out the operator’s workflow for responding to alerts and determined what additional context would help—e.g., showing which segments of the voltage waveform deviated from normal, overlaying the historical sensor signature of a typical HIGF event, or providing a simplified “confidence level” (e.g., 85% chance a HIGF is present).
    - **Mitigation:** They built a real‐time monitoring dashboard. When the DNN flags a HIGF, the dashboard automatically plots the raw voltage/current traces over the last few seconds, highlights the anomaly, and displays the model’s soft‐output probability. Operators can then cross‐check this visual evidence before deciding whether to dispatch a field crew or perform a manual inspection.
    - **Documentation:** The team captured mock‐ups of the dashboard interface, wrote user‐stories detailing how an operator would interpret each element, and recorded a rationale for every transparency feature (e.g., “We include the probability bar so that operators understand the model’s confidence and can decide a threshold at which to dispatch a crew”).
4. **Data Drift**
    - **Context:** Distribution feeder characteristics differ by geography (e.g., line impedance, typical load profiles) and climate (temperature, humidity, seasonal load variations). Even within the same grid, sensor calibrations can drift over months or years. As a result, the DNN trained on Year-1 data from Grid-A might slowly lose accuracy if deployed unchanged in Year 3 on Grid-B, or even in Year 2 on Grid-A after hardware upgrades.
    - **Assessment:** The lead data scientist cataloged plausible causes of distribution shifts—grid topology changes, seasonal temperature swings, new equipment installations, or grid expansions. They agreed that any retraining strategy should account for both:
        1. **Planned shifts** (e.g., “When moving from Grid-A to Grid-B, collect at least two weeks of labeled data under normal and HIGF conditions, then fine‐tune the model.”)
        2. **Unplanned drift** (e.g., “Install a drift detector that computes the distance between the feature‐space distribution of incoming data and the original training distribution every 30 days. If Kullback–Leibler divergence exceeds 0.1, trigger a retraining alert.”)
    - **Mitigation:** They implemented a two‐tiered approach:
        - **Periodic Model Health Checks:** Every month, the system samples a subset of recent sensor logs and compares statistical descriptors (mean, variance, spectral content) against the Year-1 baseline using a predefined similarity metric.
        - **On‐Demand Retraining:** If the drift detector fires an alarm, the operations team collects roughly 1,000 new labeled examples (half HIGF, half normal) from the current grid, augments them as needed, and retrains or fine-tunes the DNN.
    - **Documentation:** A “drift‐management playbook” was drafted, specifying: how to compute distribution‐similarity metrics; the exact trigger threshold; data‐collection procedures; labeling guidelines; and a timelinefor model‐retraining and re‐deployment.
        

By walking through these four hazards—each representative of a different AI lifecycle stage—the case study demonstrates how AIHM systematically filters out irrelevant risks, quantifies relevant ones, prescribes concrete mitigation steps, and enforces comprehensive documentation. This ensures that, as the DNN‐based HIGF detector moves from prototype to production, operators and auditors can trace every decision, verify that performance remains within acceptable bounds, and adapt to changing grid conditions over time.