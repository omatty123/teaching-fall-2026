// All situations, organizations, policies, and outcome branches are fictional.
// Outcomes are possibilities for discussion, not predictions or moral scores.
export const SIMULATIONS = [
  {
    id: "coaching",
    title: "The final team place",
    field: "Coaching and team leadership",
    role: "Assistant coach",
    setup: [
      "You help select athletes for a weekend showcase. Readiness and practice attendance were announced as selection criteria. Two athletes are similarly prepared; one has missed more practices.",
      "That athlete privately tells you their work schedule changed. They ask you not to discuss their family circumstances. Your supervisor wants the final list today."
    ],
    facts: ["The attendance difference is documented.", "No exception process was announced.", "You recommend selections; the supervisor makes the decision."],
    unknowns: ["Other athletes may also face constraints.", "You do not know whether the criteria allow exceptions."],
    people: ["The athlete requested privacy; this does not establish every detail of their situation.", "You may feel sympathy or pressure to appear consistent.", "Other athletes have an interest in a fair process."],
    choices: [
      {
        id: "criteria",
        label: "Recommend the published criteria",
        detail: "Keep the selection rule and arrange a private conversation about future participation.",
        outcomes: [
          {label: "The rule is accepted", immediate: "The supervisor uses the announced criteria and explains the selection.", later: "Athletes may trust the consistency, while unequal access to practice remains."},
          {label: "The athlete withdraws", immediate: "The athlete hears the decision as indifference to their circumstances.", later: "The team may lose a participant without understanding the obstacle."}
        ],
        analysis: "Consistency matters, but identical treatment can preserve unequal opportunities. A supportive conversation does not automatically make the selection fair.",
        newInformation: "The athlete says they can attend a different practice time next month.",
        followups: [
          {id: "schedule", label: "Propose a general scheduling review", feedback: "This addresses a recurring barrier without disclosing private details. Include other athletes before assuming one change solves the problem."},
          {id: "individual", label: "Arrange individual practice support", feedback: "Immediate support may preserve participation. Check whether comparable help is available to others who need it."}
        ]
      },
      {
        id: "review",
        label: "Request a consistent exception process",
        detail: "Ask for a brief delay and a private way for all athletes to explain constraints.",
        outcomes: [
          {label: "A review is possible", immediate: "The supervisor agrees to consider exceptions using common criteria.", later: "The process may become fairer, but athletes need clarity about future rules."},
          {label: "The deadline remains", immediate: "The supervisor says the roster cannot wait for a full review.", later: "An unfinished process may increase uncertainty and disappointment."}
        ],
        analysis: "A general process can protect both care and consistency. It still needs clear limits and confidential handling.",
        newInformation: "The organizer permits a one-day extension, but only one person can join.",
        followups: [
          {id: "review-all", label: "Review both candidates under common criteria", feedback: "The extension enables a more informed decision. Explain the criteria without revealing either athlete's circumstances."},
          {id: "retain", label: "Retain this roster and revise future rules", feedback: "This avoids changing the process at the final moment. It also leaves the present disadvantage unresolved."}
        ]
      },
      {
        id: "exception",
        label: "Recommend an individual exception",
        detail: "Request flexibility without sharing the athlete's private explanation.",
        outcomes: [
          {label: "The exception is approved", immediate: "The supervisor selects the athlete without asking for personal details.", later: "Other athletes may reasonably want to know how exceptions are decided."},
          {label: "More details are demanded", immediate: "The supervisor requests information you have not been authorized to share.", later: "The athlete's trust may be damaged if you disclose it."}
        ],
        analysis: "Care for one person does not remove obligations to others. Protecting privacy also limits how you justify an exception.",
        newInformation: "Another athlete reports that they also rearranged work to attend practice.",
        followups: [
          {id: "reconsider", label: "Request a review of both situations", feedback: "New information challenges the original comparison. Apply a common process and limit requests for personal disclosure."},
          {id: "defend", label: "Maintain the exception recommendation", feedback: "You may still have reasons to recommend flexibility. State a criterion others could use, rather than relying on sympathy alone."}
        ]
      }
    ]
  },
  {
    id: "marketing",
    title: "A customer quote for tomorrow",
    field: "Customer service and marketing",
    role: "Marketing intern",
    setup: [
      "A customer sent an enthusiastic message to help your team improve a service. Your supervisor wants the message in tomorrow's campaign. Removing the name would leave a distinctive detail about the customer's experience.",
      "This fictional organization's policy requires permission before publishing customer quotations. The customer has not answered your request. Approved aggregate survey results are also available."
    ],
    facts: ["The original message was internal feedback.", "Publication permission has not been received.", "The campaign can run without a quotation."],
    unknowns: ["The customer may not have seen the request.", "Removing the name may not prevent recognition."],
    people: ["Your supervisor is responsible for a visible deadline.", "Silence does not establish the customer's wishes.", "You may feel reluctant to delay work as an intern."],
    choices: [
      {
        id: "permission",
        label: "Wait for permission to use the quote",
        detail: "Prepare the campaign without it and keep one clear request open.",
        outcomes: [
          {label: "Permission arrives", immediate: "The customer approves a specific edited quotation.", later: "Clear agreement may support trust and future cooperation."},
          {label: "There is no reply", immediate: "The campaign launches without the personal endorsement.", later: "The team may need better ways to request testimonials in advance."}
        ],
        analysis: "A deadline does not supply consent. Repeated requests can also become pressure rather than a meaningful choice.",
        newInformation: "The customer agrees only if the distinctive detail is removed.",
        followups: [
          {id: "honor", label: "Use only the agreed version", feedback: "This respects the stated limit. Verify that the edit preserves the customer's meaning."},
          {id: "omit", label: "Leave the quotation out", feedback: "Omitting it remains a valid choice. Explain that the customer was free to set conditions."}
        ]
      },
      {
        id: "aggregate",
        label: "Use the approved survey results",
        detail: "Replace the quote with a limited claim supported by the survey.",
        outcomes: [
          {label: "The alternative is accepted", immediate: "The campaign uses the survey finding with a clear description of respondents.", later: "The team gains a reusable source of claims without exposing one customer."},
          {label: "The claim is overstated", immediate: "A colleague rewrites the finding as a promise about every customer.", later: "Readers may form expectations the evidence does not support."}
        ],
        analysis: "Aggregate evidence can protect privacy without guaranteeing accuracy. The wording still needs to match what was measured.",
        newInformation: "The survey includes only customers who completed the service.",
        followups: [
          {id: "qualify", label: "State who answered the survey", feedback: "This makes the evidence's limit visible. It does not establish the views of people who stopped using the service."},
          {id: "describe", label: "Describe the service without an outcome claim", feedback: "A factual description may be less persuasive but more supportable. Check its accuracy too."}
        ]
      },
      {
        id: "anonymous",
        label: "Propose an anonymous shortened quote",
        detail: "Offer your supervisor a draft that removes the name but keeps the distinctive detail.",
        outcomes: [
          {label: "Nobody objects", immediate: "The supervisor publishes the quotation and receives no immediate complaint.", later: "The absence of a complaint may conceal an unresolved permission problem."},
          {label: "Someone recognizes it", immediate: "A reader identifies the customer from the remaining detail.", later: "The customer may feel their feedback was used beyond its intended purpose."}
        ],
        analysis: "Anonymity and permission are different issues. A favorable response does not satisfy this organization's stated publication policy.",
        newInformation: "The campaign has been published. The customer contacts the team to say they did not approve the quotation.",
        followups: [
          {id: "withdraw", label: "Explain the gap and request prompt removal", feedback: "State that permission was not received. Check what remains in circulated copies and propose a proportionate correction."},
          {id: "review-policy", label: "Refer the complaint to the responsible lead", feedback: "Give an accurate account and request a remedy for the current use. A review of future policy does not by itself repair this disclosure."}
        ]
      }
    ]
  },
  {
    id: "finance",
    title: "Two entries that look alike",
    field: "Finance, audit, and organizational data",
    role: "Finance intern",
    setup: [
      "You prepare an expense summary for an internal board packet. Two entries have the same amount and a similar description. The supporting files are incomplete, so they might be a duplicate or separate purchases.",
      "Your supervisor asks you to mark the summary as checked before a meeting. You can flag an unresolved item, but you cannot approve payments or decide that misconduct occurred."
    ],
    facts: ["Two entries appear similar.", "The missing documents could distinguish them.", "No evidence currently establishes intentional wrongdoing."],
    unknowns: ["The entries may concern separate purchases.", "The board may rely on the total for a decision."],
    people: ["The person who entered the records has not been consulted.", "Your supervisor faces a deadline, but their reason for rushing is unclear.", "You may fear appearing inexperienced."],
    choices: [
      {
        id: "flag",
        label: "Submit a clearly provisional summary",
        detail: "Identify the unresolved entries and separate verified information from the open question.",
        outcomes: [
          {label: "The limitation is discussed", immediate: "The supervisor carries the uncertainty into the meeting.", later: "Decision-makers may wait for confirmation before relying on that portion."},
          {label: "The note is overlooked", immediate: "The summary is circulated while its qualification receives little attention.", later: "The total may be repeated as settled information."}
        ],
        analysis: "Honest labeling protects accuracy only if readers can notice it. Avoid describing an unresolved discrepancy as fraud.",
        newInformation: "A colleague's draft slide shows the total without your qualification.",
        followups: [
          {id: "correct-slide", label: "Request a visible qualification on the slide", feedback: "The correction makes uncertainty harder to miss. Confirm that the meeting materials use the revised version."},
          {id: "notify", label: "Notify the supervisor before presentation", feedback: "This uses the reporting line and gives context. Check whether the message reaches the person presenting."}
        ]
      },
      {
        id: "verify",
        label: "Request a short verification period",
        detail: "Contact the records owner and explain what can be delivered before the meeting.",
        outcomes: [
          {label: "Documents arrive", immediate: "The records owner provides information that resolves the apparent duplication.", later: "A documented check may prevent the same confusion next month."},
          {label: "Verification takes longer", immediate: "The missing files remain unavailable at meeting time.", later: "The supervisor may need a partial report instead of the promised complete total."}
        ],
        analysis: "Further checking can prevent both error and unfair suspicion. Time spent checking also needs a clear stopping point.",
        newInformation: "One receipt arrives, but the second purchase still lacks documentation.",
        followups: [
          {id: "partial", label: "Report the verified portion and remaining gap", feedback: "Partial evidence improves the report without settling everything. Keep the unresolved amount clearly identified."},
          {id: "defer", label: "Recommend deferring the affected decision", feedback: "Deferral may be proportionate if the uncertainty matters greatly. Explain its cost as well as its benefit."}
        ]
      },
      {
        id: "consult",
        label: "Seek a confidential second review",
        detail: "Ask an authorized finance lead how to handle the unresolved entries.",
        outcomes: [
          {label: "Review clarifies the process", immediate: "The finance lead identifies the appropriate check and reporting language.", later: "The team may establish a clearer process for future discrepancies."},
          {label: "The supervisor feels bypassed", immediate: "Your supervisor asks why another reviewer became involved.", later: "Working trust may require an explanation of your purpose and limits."}
        ],
        analysis: "Seeking support can be responsible under unequal authority. Share only necessary information and describe evidence without accusations.",
        newInformation: "The finance lead confirms that unresolved entries must remain visibly provisional.",
        followups: [
          {id: "align", label: "Explain the requirement to your supervisor", feedback: "This gives a clear reason for your approach. Keep the conversation about the report, not presumed motives."},
          {id: "joint", label: "Request a brief joint review", feedback: "A shared conversation may prevent conflicting instructions. It also requires time and a clear account of the remaining issue."}
        ]
      }
    ]
  },
  {
    id: "arts",
    title: "One concert, two possible rooms",
    field: "Music and arts administration",
    role: "Arts-program assistant",
    setup: [
      "You help organize a free community concert. The reserved upstairs room has 100 seats and no step-free entrance. A smaller ground-floor room has 55 seats. Some performers and attendees have said they cannot use stairs.",
      "The director must approve any room change. Moving the whole concert limits attendance; dividing the program requires extra staff and equipment. Publicity is ready, but has not been sent."
    ],
    facts: ["The upstairs room is inaccessible to some intended participants.", "The ground-floor room is available.", "The budget has little room for additional equipment."],
    unknowns: ["Actual attendance is uncertain.", "Participants may value different aspects of a split program."],
    people: ["Participants have stated an access need; no medical explanation is necessary.", "Staff may worry about extra work or disappointing attendees.", "You cannot promise a new arrangement without approval."],
    choices: [
      {
        id: "move",
        label: "Recommend moving the whole concert",
        detail: "Use the ground-floor room and propose a transparent reservation process.",
        outcomes: [
          {label: "The smaller room is sufficient", immediate: "The director approves the move and most interested people obtain seats.", later: "Participants may value attending the same event together."},
          {label: "Demand exceeds capacity", immediate: "Some people cannot reserve a place.", later: "The allocation process may create a new fairness concern."}
        ],
        analysis: "A shared accessible space addresses a concrete exclusion. Limited capacity still requires a defensible allocation process.",
        newInformation: "Reservation requests exceed 55, and several people cannot use the online form.",
        followups: [
          {id: "access-reservations", label: "Add phone reservations and a waitlist", feedback: "This reduces one barrier to requesting a seat. Apply the same allocation rule across both methods."},
          {id: "repeat", label: "Propose a second performance", feedback: "Another performance could increase access. Confirm performers' consent, workload, and resources before announcing it."}
        ]
      },
      {
        id: "split",
        label: "Propose two coordinated performance spaces",
        detail: "Check whether a shared program can work in both rooms within available resources.",
        outcomes: [
          {label: "Coordination works", immediate: "Staff and performers develop a feasible program across both spaces.", later: "More people may attend, though their experiences differ."},
          {label: "The smaller program becomes secondary", immediate: "Limited equipment and staffing reduce the ground-floor offering.", later: "An arrangement described as inclusive may leave some participants excluded from key performances."}
        ],
        analysis: "Using both rooms does not itself establish equal participation. Compare the actual experiences instead of relying on the arrangement's label.",
        newInformation: "The same audio equipment cannot serve both rooms simultaneously.",
        followups: [
          {id: "equipment-loan", label: "Seek an approved equipment loan", feedback: "A loan could improve the ground-floor program. Confirm staffing and participant access before treating equipment as the only barrier."},
          {id: "one-room", label: "Recommend one accessible room instead", feedback: "This simplifies coordination and keeps the program together. Address the resulting capacity limit openly."}
        ]
      },
      {
        id: "consult",
        label: "Request a short planning delay",
        detail: "Consult affected participants and staff before recommending a room arrangement.",
        outcomes: [
          {label: "Consultation changes the plan", immediate: "Participants identify practical needs the original discussion missed.", later: "The revised arrangement may offer more meaningful access."},
          {label: "Planning remains unresolved", immediate: "Responses arrive slowly while publicity and staffing decisions wait.", later: "Delay may reduce attendance or make an otherwise feasible plan harder."}
        ],
        analysis: "Listening supports informed care without requiring personal disclosures. Consultation should have a clear deadline and genuine influence on the decision.",
        newInformation: "Participants prefer one shared room, but the director has not approved reduced capacity.",
        followups: [
          {id: "recommend", label: "Present that preference with a capacity plan", feedback: "This translates consultation into a concrete recommendation. Explain remaining disagreements rather than claiming unanimous support."},
          {id: "contingency", label: "Request a decision and an accessible fallback", feedback: "A deadline prevents indefinite delay. The fallback must still address the stated exclusion."}
        ]
      }
    ]
  },
  {
    id: "public-works",
    title: "Which stops get new benches",
    field: "Construction and public works",
    role: "Public-works planning intern",
    setup: [
      "Your department can install two new bus-stop benches. You are asked to recommend locations using complaint records. One neighborhood has sent many requests; another busy route has few recorded complaints and little seating.",
      "The records count messages, not unique residents or daily riders. Staff can make a limited site visit this week. Your recommendation will go to a supervisor, who controls the installation schedule."
    ],
    facts: ["Resources cover two benches.", "Complaint totals do not measure ridership.", "Some requests may come from the same people."],
    unknowns: ["People may face different barriers to making requests.", "You do not yet have comparable observations at each stop."],
    people: ["Frequent complainants have made their concerns visible.", "People who have not written may still need seating.", "You may feel pressure to produce a simple ranking."],
    choices: [
      {
        id: "requests",
        label: "Rank the recorded requests",
        detail: "Use the existing information while stating what it cannot establish.",
        outcomes: [
          {label: "The ranking is accepted", immediate: "The department responds quickly to documented concerns.", later: "People with easier access to complaint channels may continue receiving more attention."},
          {label: "The ranking is challenged", immediate: "A resident points out that repeated messages inflated one location's total.", later: "Trust may depend on whether the department corrects the comparison."}
        ],
        analysis: "Responsiveness to requests matters, but message volume is not the same as need. A limitation should affect interpretation, not merely appear in a footnote.",
        newInformation: "Several requests concern the same stop and come from one household.",
        followups: [
          {id: "deduplicate", label: "Revise the count and explain its limits", feedback: "This corrects a misleading comparison. Unique-request counts still do not represent every rider."},
          {id: "add-observation", label: "Add a limited observation before recommending", feedback: "A site visit supplies another kind of evidence. State its time, scope, and limits."}
        ]
      },
      {
        id: "observe",
        label: "Collect comparable observations",
        detail: "Ask for brief visits at the same times and invite comments through more than one channel.",
        outcomes: [
          {label: "Patterns become clearer", immediate: "Visits reveal substantial use at a stop with few complaints.", later: "The recommendation may better reflect needs absent from the written record."},
          {label: "The sample is misleading", immediate: "Weather or an unusual event affects the observed use.", later: "A small study may acquire more authority than its evidence supports."}
        ],
        analysis: "Additional evidence can improve a decision without making it complete. Explain uncertainty and avoid treating a short visit as representative of every day.",
        newInformation: "The proposed installation date allows one extra week of observation.",
        followups: [
          {id: "broaden", label: "Sample different days and times", feedback: "Broader observation can test the initial pattern. Keep the method comparable across candidate locations."},
          {id: "provisional", label: "Offer a provisional recommendation now", feedback: "A provisional decision may preserve the schedule. Identify what new evidence would change it."}
        ]
      },
      {
        id: "share",
        label: "Recommend one bench on each route",
        detail: "Propose geographic distribution while acknowledging incomplete evidence about demand.",
        outcomes: [
          {label: "Distribution is welcomed", immediate: "Both routes receive a visible improvement.", later: "Residents may see the allocation as recognition of shared needs."},
          {label: "Equal shares miss unequal needs", immediate: "One selected stop serves few riders while a crowded stop remains without seating.", later: "Equal distribution may leave the larger unmet need unchanged."}
        ],
        analysis: "Equal shares are one possible fairness principle, not an automatic solution. State why that principle fits the available evidence.",
        newInformation: "A routine count suggests that one route has substantially more riders.",
        followups: [
          {id: "reassess", label: "Reassess the allocation using the count", feedback: "New evidence may justify different shares. Check whether the count covers comparable periods."},
          {id: "retain-spread", label: "Retain the geographic distribution with reasons", feedback: "Broad coverage may still matter alongside ridership. Explain the need you prioritize and the need left unmet."}
        ]
      }
    ]
  },
  {
    id: "research",
    title: "A program's missing responses",
    field: "Education and policy research",
    role: "Program-research intern",
    setup: [
      "You summarize feedback on an after-school program. Most survey respondents attend regularly and report benefits. Families who stopped attending rarely answered. A funding application needs a short findings section this week.",
      "The team also has approved, anonymous attendance totals. You can describe those totals, but they do not explain why participants left. Your supervisor hopes the research will support continued funding."
    ],
    facts: ["Respondents are mainly regular participants.", "Some former participants are missing from the survey.", "Attendance totals contain no explanations for leaving."],
    unknowns: ["Nonresponse may have several causes.", "The benefits reported by respondents may not describe everyone."],
    people: ["Current participants value the program, according to their responses.", "Staff have an interest in continued funding.", "Families may have reasons for declining further contact."],
    choices: [
      {
        id: "bounded",
        label: "Report the positive findings with clear limits",
        detail: "Identify whose responses support the claim and whose views are missing.",
        outcomes: [
          {label: "Limits are taken seriously", immediate: "The application describes benefits reported by respondents without claiming universal success.", later: "Funders may support the work while requesting better evidence."},
          {label: "The qualification disappears", immediate: "An editor keeps the positive sentence but removes the response limitation.", later: "Readers may mistake a selected group's experience for the whole program."}
        ],
        analysis: "Limited evidence can still be useful when its scope is visible. A worthy program does not justify a broader claim than the evidence supports.",
        newInformation: "The final draft says the program benefits every participating family.",
        followups: [
          {id: "correct", label: "Request wording tied to the respondents", feedback: "This restores the connection between evidence and claim. Check the final version before circulation."},
          {id: "separate", label: "Add a distinct evidence-and-limits paragraph", feedback: "A separate paragraph can make missing evidence visible. It must also correct the unsupported universal statement."}
        ]
      },
      {
        id: "follow-up",
        label: "Request time for voluntary follow-up",
        detail: "Seek missing perspectives without promising benefits or pressuring families to answer.",
        outcomes: [
          {label: "More perspectives arrive", immediate: "Some former participants describe obstacles the initial survey did not capture.", later: "The program may improve even if the findings become less uniformly positive."},
          {label: "Few people respond", immediate: "Additional contact produces little new information before the deadline.", later: "The report still has gaps, and repeated requests may burden families."}
        ],
        analysis: "Listening to missing participants can improve both research and care. Their choice not to respond must remain meaningful.",
        newInformation: "The application allows a later research supplement, but its first deadline remains.",
        followups: [
          {id: "supplement", label: "Submit limited findings and plan the supplement", feedback: "This separates the funding deadline from unfinished research. Do not promise that more responses will confirm the initial findings."},
          {id: "stop-contact", label: "End repeated contact and document the gap", feedback: "Stopping can respect participants' time and choices. The remaining uncertainty must stay visible in the report."}
        ]
      },
      {
        id: "attendance",
        label: "Combine survey findings with attendance totals",
        detail: "Report participation patterns alongside the survey without inventing reasons for leaving.",
        outcomes: [
          {label: "The evidence is kept distinct", immediate: "Readers see both reported benefits and changes in participation.", later: "The team can identify areas for further investigation without claiming causes."},
          {label: "A cause is assumed", immediate: "A colleague describes lower attendance as proof of family disinterest.", later: "That interpretation may direct improvements away from actual barriers."}
        ],
        analysis: "Combining sources does not make them answer the same question. Attendance counts show participation, not motives or satisfaction.",
        newInformation: "A staff member mentions a recent transport change that was not included in the survey.",
        followups: [
          {id: "test-explanation", label: "Record transport as a possible explanation", feedback: "The report can identify a reason to investigate. It should not present the suggestion as a confirmed cause."},
          {id: "descriptive", label: "Keep the current report descriptive", feedback: "Staying descriptive avoids unsupported causal claims. Preserve the transport issue for later inquiry rather than dismissing it."}
        ]
      }
    ]
  }
];
