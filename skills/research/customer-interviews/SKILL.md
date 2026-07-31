---
name: customer-interviews
version: '1.0'
last_updated: 2026-03-25
author: genesys-growth
description: 'Generates structured interview guides for five B2B SaaS research types: discovery, win/loss, churn, expansion,
  and testimonial. Produces a ready-to-use guide with preparation checklist, tailored question bank, probing follow-ups, and
  a synthesis framework that maps findings directly to icp-research sections. Triggers: "customer interview", "interview guide",
  "interview questions", "user research questions", "customer discovery calls", or preparing for any customer conversation.
  Upstream: recommended company-context, icp-research. Downstream: feeds icp-research, icp-behavioural, win-loss-analysis,
  and case-study. NOT for analyzing completed interviews (use /transcript-analysis) or sales discovery calls (use /client-discovery).'
goal: 'Generates structured interview guides for five B2B SaaS research types: discovery, win/loss, churn, expansion, and
  testimonial.'
outcome: 'Generates structured interview guides for five B2B SaaS research types: discovery, win/loss, churn, expansion, and
  testimonial. Produces a ready-to-use guide with preparation checklist, tailored question bank, probing follow-ups, and a
  synthesis framework that maps findings directly to...'
primitive: research
ontology_type: transcript-insights
review_gate: 1
inputs:
  required: []
  recommended:
  - company-context
  - icp-research
- type: interview-guide
  feeds_into:
  - icp-research
  - icp-behavioural
  - positioning
  - win-loss-analysis
depends_on: []
- icp-behavioural
- icp-research
- positioning
- win-loss-analysis
owned_by_agent: researcher
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /customer-interviews
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Customer interviews skill

Prepare structured interview guides for B2B SaaS customer research. Produces question banks, preparation frameworks, and synthesis templates that feed directly into ICP research and positioning work.

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| Interview type | Yes | User specifies: discovery, win/loss, churn, expansion, or testimonial |
| Company context | Recommended | `/company-context` output or client CLAUDE.md |
| ICP profile | Recommended | `/icp-research` output |
| Specific research goals | Yes | User states what they're trying to learn |

## Interview types

Full question banks (10-15 questions per type) live in the premium reference. Use this table to pick the right type, then pull 8-12 questions from the bank.

| Type | Purpose | When to use |
|------|---------|-------------|
| **1. Discovery** | Understand the prospect's world before they became a customer. Map pain, workflow, buying triggers, decision criteria. | Early-stage ICP research, entering new segments, validating positioning hypotheses |
| **2. Win/loss** | Understand why deals closed (or didn't). Extract decision criteria, competitive dynamics, buying process details. | After closed-won/closed-lost deals, competitive positioning, sales enablement |
| **3. Churn** | Understand why customers left. Identify product gaps, service failures, unmet expectations. | After churn events, retention strategy, product feedback loops |
| **4. Expansion** | Understand what drives upsell, cross-sell, seat expansion. Map the internal champion's advocacy process. | Expansion playbook development, pricing research, PLG analysis |
| **5. Testimonial** | Extract quotable results, transformation stories, social proof. | Case study production, social proof gathering, website copy refresh |

## Preparation framework

Run this checklist before every interview.

### 1. Research the interviewee

- [ ] Role, title, tenure at company
- [ ] LinkedIn profile review (career path, posts, interests)
- [ ] Their company's stage, size, industry
- [ ] Any previous interactions with your team (sales notes, support tickets, NPS scores)
- [ ] Public content they've produced (blog posts, conference talks, comments)

### 2. Define research goals

- [ ] What are the 3 specific things you need to learn from this conversation?
- [ ] What hypotheses are you testing?
- [ ] What gaps in your current ICP/positioning/competitive data does this fill?
- [ ] How will you use the output? (Which downstream skill or deliverable?)

### 3. Customize the question bank

- [ ] Select 8-12 questions from the relevant interview type
- [ ] Reorder based on priority (most important questions early, in case you run short)
- [ ] Personalize with company-specific details ("I noticed you switched from [competitor]...")
- [ ] Prepare 2-3 follow-up probes for each key question
- [ ] Remove questions you already have answers to

### 4. Logistics

- [ ] Interview length: 30-45 minutes (never over 60)
- [ ] Recording permission: ask at the start, not mid-conversation
- [ ] Note-taker: assign someone or use transcription (Granola, Otter, etc.)
- [ ] Warm-up plan: 2-3 minutes of genuine rapport before questions

## During the interview

### Principles

- **Listen more than you talk.** Target 80/20 ratio (them/you).
- **Follow the energy.** When they lean into a topic, go deeper. Your script is a guide, not a cage.
- **Ask "why" and "tell me more" liberally.** The best insights come from the second and third layers.
- **Use their words, not yours.** Don't rephrase their pain into your product language.
- **Sit in the silence.** When they pause, don't fill the gap. They're often about to say the most honest thing.
- **Capture exact quotes.** Flag verbatim language in your notes with quotation marks. These are gold for messaging.

### Follow-up prompts

Use these when an answer is surface-level:

- "Can you give me a specific example of that?"
- "What happened next?"
- "How did that make you feel?"
- "Who else was affected by that?"
- "What would have happened if you hadn't done anything?"
- "Help me understand the timeline on that."
- "You mentioned [X] -- say more about that?"

### Red flags during interviews

- They're giving you the answers they think you want. Redirect with "I really want the honest version."
- They're speaking in generalities. Push for specifics: "When was the last time that happened?"
- They're selling you on their company. Gently steer back: "That's helpful context. Now tell me about the problem side."
- You're asking leading questions. Catch yourself. "Don't you think X is a problem?" becomes "How do you think about X?"

## Synthesis framework

After the interview, map findings to these categories. Each one feeds directly into downstream skills.

| Category | Feeds into | What to capture |
|----------|------------|-----------------|
| **Pain points and triggers** | icp-research, positioning | Specific problems described; what triggered the search; urgency / cost of inaction |
| **Buying process** | icp-research, win-loss-analysis | Who was involved; evaluation process; timeline and friction points |
| **Decision criteria** | positioning, product-messaging | What mattered most; deal-breakers; how alternatives were compared |
| **Language and vocabulary** | tone-of-voice, messaging | Exact phrases for the problem; how they describe the solution to peers; words they avoid |
| **Results and impact** | case-study, testimonial content | Quantifiable outcomes; qualitative changes; before/after contrast |
| **Objections and concerns** | sales-enablement, battlecards | What almost stopped them buying; concerns remaining; what they'd change |

## Anti-patterns

**Don't do these:**

- Asking yes/no questions. Every question should be open-ended.
- Running through all 15 questions in 30 minutes. Pick 8-12 and go deep.
- Recording without permission. Always ask first, and respect a "no."
- Interviewing through a screen share of your product. This is research, not a demo.
- Combining interviews with sales pitches. Keep them separate or you'll poison the data.
- Interviewing only happy customers. Churned users and lost deals are where the real insights live.
- Skipping synthesis. Raw notes decay fast. Synthesize within 24 hours or the context fades.
- Treating one interview as truth. A single data point is an anecdote. You need 5-8 interviews per segment to see patterns.

