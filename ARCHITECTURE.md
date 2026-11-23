# How shilaycow works

This document explains the harness as a system: what it is made of, what it guarantees, how a task moves from an idea to a merged pull request, and where it can break. The skills themselves (`plugin/skills/*/SKILL.md`) are the exact instructions the agent follows; this is the map that shows how they fit together.

**Contents**

1. [The idea in one paragraph](#1-the-idea-in-one-paragraph)
2. [Three layers](#2-three-layers)
3. [The boundary: what the agent cannot do](#3-the-boundary-what-the-agent-cannot-do)
4. [Levels: how much the agent merges on its own](#4-levels-how-much-the-agent-merges-on-its-own)
5. [Roles: Owner, Chief, builder, verifier](#5-roles-owner-chief-builder-verifier)
6. [The life of a task](#6-the-life-of-a-task)
7. [Verification: how a verdict is reached](#7-verification-how-a-verdict-is-reached)
8. [When the agent stops and asks](#8-when-the-agent-stops-and-asks)
9. [Learning: guards that grow from real mistakes](#9-learning-guards-that-grow-from-real-mistakes)
10. [What appears in your repository](#10-what-appears-in-your-repository)
11. [Where state lives, and how a run resumes](#11-where-state-lives-and-how-a-run-resumes)
12. [When it breaks, and how to recover](#12-when-it-breaks-and-how-to-recover)

---

## 1. The idea in one paragraph

Give the agent as much freedom as possible, and protect only what a mistake could cost you. The protection lives on GitHub's servers, not in instructions the agent has to read and obey: the agent works as a bot account that simply has no permission to change `main`. Inside that boundary, quality is not bought by prescribing steps. It comes from checking results: an independent session that built none of the work tries it the way a user would, breaks each behaviour to see the tests fail, and reads the code as its future maintainer.

Two kinds of rule follow from this, and every rule in the harness is one or the other:

| Kind | It does | Where it lives | Can the agent skip it? |
|---|---|---|---|
| **Guard** | limits what a mistake can cost | GitHub (server side) wherever possible | No |
| **Advice** | describes a way of working that tends to go well | the skills | Yes, with judgement |

---

## 2. Three layers

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Segoe UI, sans-serif","fontSize":"14px","lineColor":"#6B7280","primaryTextColor":"#111827","edgeLabelBackground":"#FFFFFF","clusterBkg":"transparent"},"flowchart":{"curve":"basis","nodeSpacing":40,"rankSpacing":45,"subGraphTitleMargin":{"top":6,"bottom":22}}}}%%
flowchart TB
    subgraph G["<b>Grown guards</b><br/><small>per project, merged by you</small>"]
        direction LR
        G1["<b>Pitfalls</b><br/><small>read by every builder</small>"] --> G2["<b>Types · lint · tests</b><br/><small>after a mistake happens twice</small>"] --> G3["<b>CI checks</b><br/><small>proposed, you apply</small>"]
    end
    subgraph M["<b>Method layer</b><br/><small>knowledge, the 18 skills</small>"]
        direction LR
        M1["<b>Early</b><br/><small>sharpen · how · why · spec</small>"] --> M2["<b>Middle</b><br/><small>design · plan · prove</small>"] --> M3["<b>Late</b><br/><small>verify · try-it · blast-radius<br/>trail · report</small>"] --> M4["<b>End of cycle</b><br/><small>retro · correct</small>"]
    end
    subgraph P["<b>Permission layer</b><br/><small>fixed, enforced by GitHub</small>"]
        direction LR
        P1["<b>Bot account</b><br/><small>Write role only</small>"] ~~~ P2["<b>Ruleset on main</b><br/><small>PR + 1 approval<br/>no force push · no deletion</small>"] ~~~ P3["<b>merge_unit</b><br/><small>Level 1 to 4</small>"]
    end
    G -->|"read by the next task"| M
    M -->|"works inside"| P
    M -.->|"retro and correct propose"| G
    classDef you fill:#FFF4DB,stroke:#C98A00,stroke-width:1.5px,color:#3D2B00
    classDef agent fill:#E6F0FF,stroke:#2F6FDB,stroke-width:1.5px,color:#0B2552
    classDef gh fill:#E3F6E8,stroke:#2E8B57,stroke-width:1.5px,color:#0D3B22
    classDef gate fill:#FFFFFF,stroke:#C98A00,stroke-width:2px,color:#3D2B00
    classDef stop fill:#FDECEC,stroke:#C0392B,stroke-width:1.5px,color:#5A1410
    classDef neutral fill:#F1F3F6,stroke:#8A94A6,stroke-width:1.5px,color:#1F2633
    class P1,P2,P3 neutral
    class M1,M2,M3,M4 agent
    class G1,G2,G3 gh
    style P fill:#F7F8FA,stroke:#B8C0CC,stroke-dasharray:4 3,color:#3A4352
    style M fill:#F5F9FF,stroke:#9DBBF0,stroke-dasharray:4 3,color:#1D4A99
    style G fill:#F4FBF6,stroke:#9AD1B0,stroke-dasharray:4 3,color:#1E6B41
```

- **The permission layer** is set up once per repository with `shilaycow-setup` and never changes between levels.
- **The method layer** is the same at every level. At Level 1 you call the skills yourself; from Level 2 up, the Chief calls the same skills.
- **Grown guards** belong to no level. A new project ships with none; each one is added because a mistake actually happened twice in that project.

---

## 3. The boundary: what the agent cannot do

Every action with a large blast radius (irreversible, external, or costly) gets exactly one guard, placed on the server whenever possible.

| Action | Why it is dangerous | Guard | Strength |
|---|---|---|---|
| Changing `main` | the one thing you cannot throw away | Ruleset: pull request required, one approval, no force push, no deletion. The bot opens the pull request, and GitHub does not let an author approve their own | Server side |
| Changing settings, rulesets or collaborators | would remove the guard above | the bot has the Write role, not Admin | Server side |
| Changing CI workflows | could disable required checks | the bot's credentials carry no workflow permission | Server side |
| Reading or leaking secrets | cannot be taken back | the cloud environment holds no secrets | Configuration |
| External side effects (deploy, email, paid APIs) | cannot be taken back | the environment's network allows package registries only; no deploy credentials | Configuration |
| Runaway spending | money and quota | each task has an hours and sessions budget | Written rule |
| Touching another session's branch | destroys someone else's work | each session pushes only its own branch; only the Chief merges into the task branch | Written rule |

**Deliberately not guarded:** files outside a ticket's scope, test configuration, commit authorship, destructive commands inside the container. All of these happen on a branch you can delete or in a container that is thrown away. If one of them keeps causing trouble in your project, it becomes that project's own guard (section 9).

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Segoe UI, sans-serif","fontSize":"14px","lineColor":"#6B7280","primaryTextColor":"#111827","edgeLabelBackground":"#FFFFFF","clusterBkg":"transparent"},"flowchart":{"curve":"basis","nodeSpacing":40,"rankSpacing":45,"subGraphTitleMargin":{"top":6,"bottom":22}}}}%%
flowchart LR
    A["<b>Agent</b><br/><small>acts as the bot</small>"] -->|"push"| B["<b>task/ or work/ branch</b><br/><small>disposable</small>"]
    B -->|"opens"| PR["<b>Pull request into main</b>"]
    PR -->|"independent session"| V["<b>Verdict</b><br/><small>PASS or FAIL on one commit</small>"]
    V --> O{{"<b>You</b> read, try, decide"}}
    O ==>|"merge"| MAIN[("<b>main</b>")]
    O -.->|"send back"| B
    A -. "push to main<br/>refused by the ruleset" .-x MAIN
    A -. "change settings<br/>refused, Write role only" .-x S["<b>Repository settings</b>"]

    classDef you fill:#FFF4DB,stroke:#C98A00,stroke-width:1.5px,color:#3D2B00
    classDef agent fill:#E6F0FF,stroke:#2F6FDB,stroke-width:1.5px,color:#0B2552
    classDef gh fill:#E3F6E8,stroke:#2E8B57,stroke-width:1.5px,color:#0D3B22
    classDef gate fill:#FFFFFF,stroke:#C98A00,stroke-width:2px,color:#3D2B00
    classDef stop fill:#FDECEC,stroke:#C0392B,stroke-width:1.5px,color:#5A1410
    classDef neutral fill:#F1F3F6,stroke:#8A94A6,stroke-width:1.5px,color:#1F2633
    class A,B,V agent
    class PR neutral
    class O gate
    class MAIN gh
    class S stop
```

The boundary holds without the agent reading a single word. That is why it is the only thing the harness insists on.

---

## 4. Levels: how much the agent merges on its own

Every level is measured with one ruler: **what is the unit you, the owner, merge?** It is one value in the config:

```yaml
# .shilaycow/config.yml
merge_unit: task     # change | ticket | milestone | task
```

| Level | `merge_unit` | You merge | The agent acts as | The agent merges, on its own | Dispatched by | Setup |
|---|---|---|---|---|---|---|
| 1 | `change` | every change | you | nothing | you, skill by skill | none |
| 2 | `ticket` | one pull request per ticket | the bot | nothing | the Chief | `shilaycow-setup` once |
| 3 | `milestone` | one pull request per milestone | the bot | tickets into `task/<slug>` | the Chief | same as Level 2 |
| 4 | `task` | one pull request per task | the bot | everything into `task/<slug>` | the Chief | same as Level 2 |

Levels 2 to 4 need the same GitHub setup; moving between them is one line in the config. At no level does the agent merge `main`.

What the branches look like at Level 4, with two tickets:

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Segoe UI, sans-serif","git0":"#2E8B57","git1":"#2F6FDB","git2":"#7AA7F0","git3":"#7AA7F0","gitBranchLabel0":"#FFFFFF","gitBranchLabel1":"#FFFFFF","gitBranchLabel2":"#0B2552","gitBranchLabel3":"#0B2552","commitLabelBackground":"#FFFFFF","commitLabelColor":"#111827"},"gitGraph":{"mainBranchName":"main"}}}%%
gitGraph
    commit id: "main"
    branch task/search
    checkout task/search
    commit id: "brief + design + plan"
    branch work/search/T-01
    checkout work/search/T-01
    commit id: "T-01 built"
    checkout task/search
    merge work/search/T-01 id: "Chief merges T-01"
    branch work/search/T-02
    checkout work/search/T-02
    commit id: "T-02 built"
    checkout task/search
    merge work/search/T-02 id: "Chief merges T-02"
    commit id: "spec + final report"
    checkout main
    merge task/search id: "You merge the task" type: HIGHLIGHT
```

At Level 3 the same thing happens once per milestone; at Level 2 each `work/` branch opens its pull request straight into `main`, and there is no `task/` branch.

---

## 5. Roles: Owner, Chief, builder, verifier

| Role | Who | Does | Never does |
|---|---|---|---|
| **Owner** | you | approves the brief, says "start", answers `needs-owner` issues, merges `main` | — |
| **Chief** | the session you start with `shilaycow-chief` | agrees the brief with you, plans, dispatches, merges tickets into the task branch, writes the report, opens the pull request into `main` | push to or merge `main`; verify its own work |
| **Builder** | a subagent of the Chief, one per ticket, in its own worktree | builds one ticket, proves each behaviour, opens a pull request, posts `Ready.` | change the brief; push outside its branch |
| **Verifier** | a new session that shares nothing with the builders | judges one head commit cold and posts `PASS` or `FAIL` | fix code, push, merge, or coach the builder |

All roles act as the same bot account, so they are told apart by session: every `Ready.` and every verdict carries a `Session:` line, and the Chief rejects a `PASS` whose session matches the Chief's own or any builder's.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Segoe UI, sans-serif","actorBkg":"#FFFFFF","actorBorder":"#8A94A6","actorTextColor":"#111827","signalColor":"#4B5563","signalTextColor":"#111827","noteBkgColor":"#FFF4DB","noteBorderColor":"#C98A00","noteTextColor":"#3D2B00","labelBoxBkgColor":"#F1F3F6","labelBoxBorderColor":"#8A94A6","loopTextColor":"#1F2633"}}}%%
sequenceDiagram
    box rgb(255,244,219) You
        actor Owner
    end
    box rgb(230,240,255) The agent, acting as the bot
        participant Chief
        participant Builder as Builder (per ticket)
        participant Verifier as Verifier (new session)
    end
    box rgb(227,246,232) GitHub
        participant GH as GitHub
    end
    Owner->>Chief: describe the task
    Chief-->>Owner: says back what it understood
    Chief->>GH: brief.md on the task branch
    Owner->>Chief: approve and say "start"
    Note over Owner,Chief: unattended from here
    Chief->>GH: tracking issue "Task: slug"
    loop each ticket, in parallel when areas do not overlap
        Chief->>Builder: roles/builder.md + the ticket
        Builder->>GH: work branch, pull request, "Ready."
        opt care level is careful, or the Chief judges it worth it
            Chief->>Verifier: roles/verifier.md + the pull request
            Verifier->>GH: "Verification: PASS / FAIL"
        end
        Chief->>GH: merge the ticket into the task branch
    end
    Chief->>GH: spec update, final report, pull request into main
    Chief->>Verifier: judge the head of that pull request
    Verifier->>GH: verdict on the exact head commit
    Chief->>GH: findings, "Retro:", "Finished:"
    GH-->>Owner: a pull request ready to try and merge
    Owner->>GH: merge, or send back
```

The builder never starts its own verifier: whoever is being judged does not write the judge's instructions.

---

## 6. The life of a task

A task has two halves with one explicit handover: **your "start"**.

- **The first half is a conversation.** `shilaycow-sharpen` says back what you asked for in its own words, then turns it into a brief of plain Given / When / Then scenarios. You can also design together here. The Chief dispatches nobody until you say start. Whatever is agreed is written to files on the task branch as you go, so nothing depends on the conversation surviving.
- **The second half is unattended.** The Chief decides everything else: whether a design is needed, how to cut the work, whether to build itself or dispatch builders, which tickets deserve their own verification.

### 6.1 The task as a state machine

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Segoe UI, sans-serif","fontSize":"14px","lineColor":"#6B7280","primaryTextColor":"#111827","edgeLabelBackground":"#FFFFFF","clusterBkg":"transparent"},"flowchart":{"curve":"basis","nodeSpacing":40,"rankSpacing":45,"subGraphTitleMargin":{"top":6,"bottom":22}}}}%%
flowchart TB
    subgraph TALK["<b>① With you</b><br/><small>a conversation</small>"]
        direction TB
        S["<b>Sharpening</b><br/><small>says it back, writes the brief</small>"]
        D["<b>Designing together</b><br/><small>optional</small>"]
        G{{"You say <b>start</b>"}}
        S -->|"you want to"| D
        D -->|"a scenario changes"| S
        S --> G
        D --> G
    end
    subgraph ALONE["<b>② Unattended</b><br/><small>the agent, acting as the bot</small>"]
        direction TB
        P["<b>Planning</b><br/><small>cut into tickets</small>"]
        B["<b>Building</b><br/><small>one builder per ticket</small>"]
        F["<b>Finishing</b><br/><small>spec + final report</small>"]
        J["<b>Judging</b><br/><small>a session that built none of it</small>"]
        X["<b>Fixing</b><br/><small>at most fix_rounds</small>"]
        P --> B
        B -->|"next ticket"| B
        B -.->|"plan was wrong"| P
        B -->|"all tickets merged"| F
        F -->|"pull request into main"| J
        J -->|"FAIL"| X
        X -->|"new head, new verdict"| J
    end
    subgraph YOURS["<b>③ Your call</b><br/><small>on GitHub</small>"]
        direction TB
        R["<b>Ready for you</b><br/><small>report + how to try it</small>"]
        M(["<b>Merged</b>"])
        R -->|"you merge"| M
    end
    G ==>|"approved"| P
    J ==>|"PASS"| R
    R -.->|"you send it back"| S

    classDef you fill:#FFF4DB,stroke:#C98A00,stroke-width:1.5px,color:#3D2B00
    classDef agent fill:#E6F0FF,stroke:#2F6FDB,stroke-width:1.5px,color:#0B2552
    classDef gh fill:#E3F6E8,stroke:#2E8B57,stroke-width:1.5px,color:#0D3B22
    classDef gate fill:#FFFFFF,stroke:#C98A00,stroke-width:2px,color:#3D2B00
    classDef stop fill:#FDECEC,stroke:#C0392B,stroke-width:1.5px,color:#5A1410
    classDef neutral fill:#F1F3F6,stroke:#8A94A6,stroke-width:1.5px,color:#1F2633
    class S,D you
    class G gate
    class P,B,F,J,X agent
    class R,M gh
    style TALK fill:#FFFBF0,stroke:#E8C877,stroke-dasharray:4 3,color:#7A5300
    style ALONE fill:#F5F9FF,stroke:#9DBBF0,stroke-dasharray:4 3,color:#1D4A99
    style YOURS fill:#F4FBF6,stroke:#9AD1B0,stroke-dasharray:4 3,color:#1E6B41
```

Two exits apply from **any** unattended state, so they are not drawn as arrows:

- **Waiting on you:** the agent needs something from the boundary table. It opens a `needs-owner` issue, carries on with whatever that does not block, and resumes the rest once you answer.
- **Stopped:** the budget is used up, the same failure survived `fix_rounds` rounds, or you wrote "stop" on the tracking issue. The run ends; starting `shilaycow-chief` again resumes from what is on GitHub (section 11).

| State | What is true | Written where |
|---|---|---|
| Sharpening | the Chief is restating and asking about outcomes only | `docs/tasks/<slug>/brief.md` |
| Approved | you said start; the level and budget are fixed for the task | first line of the tracking issue |
| Planning | the work is cut into tickets someone could pick up cold | `plan.md`, `tickets/T-nn.md` |
| Building | tickets are being built, proven and merged into the task branch | `work/<slug>/T-nn` pull requests |
| Finishing | `docs/spec/` is brought up to date, the final report is written | `docs/spec/`, `reports/final.md` |
| Judging | an independent session is checking the exact head commit | verdict comment on the pull request |
| Fixing | one fix round; at most `fix_rounds` (default 2) | a new head commit |
| Wrapping | everything after the verdict goes on GitHub, so the judged commit stays the one you merge | comments on the pull request and tracking issue |
| AwaitingOwner | a pull request you can read, try and merge | the pull request |

### 6.2 A ticket as a state machine

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Segoe UI, sans-serif","fontSize":"14px","lineColor":"#6B7280","primaryTextColor":"#111827","edgeLabelBackground":"#FFFFFF","clusterBkg":"transparent"},"flowchart":{"curve":"basis","nodeSpacing":40,"rankSpacing":45,"subGraphTitleMargin":{"top":6,"bottom":22}}}}%%
flowchart LR
    O["<b>Open</b><br/><small>written by plan</small>"] -->|"Chief dispatches"| IP["<b>In progress</b><br/><small>a builder on work/…</small>"]
    IP -->|"contradiction, wrong test,<br/>secret or deploy needed"| BL["<b>Blocked</b><br/><small>comment says why</small>"]
    BL -->|"Chief re-cuts or asks you"| O
    IP -->|"suite passes · Status: done<br/>pull request + Ready."| RD["<b>Ready</b>"]
    RD -->|"careful, or Chief asks"| JD{{"<b>Verified</b>"}}
    JD -->|"FAIL<br/>fix round"| IP
    JD -->|"PASS"| MG(["<b>Merged into<br/>the task branch</b>"])
    RD -->|"no verdict needed"| MG

    classDef you fill:#FFF4DB,stroke:#C98A00,stroke-width:1.5px,color:#3D2B00
    classDef agent fill:#E6F0FF,stroke:#2F6FDB,stroke-width:1.5px,color:#0B2552
    classDef gh fill:#E3F6E8,stroke:#2E8B57,stroke-width:1.5px,color:#0D3B22
    classDef gate fill:#FFFFFF,stroke:#C98A00,stroke-width:2px,color:#3D2B00
    classDef stop fill:#FDECEC,stroke:#C0392B,stroke-width:1.5px,color:#5A1410
    classDef neutral fill:#F1F3F6,stroke:#8A94A6,stroke-width:1.5px,color:#1F2633
    class O,IP,RD agent
    class BL stop
    class JD gate
    class MG gh
```

### 6.3 The care level

The brief has one dial between speed and assurance. It sets the least the Chief does; it may always do more.

| Care level | Suited to | At least |
|---|---|---|
| fast | prototypes, small tools | the final verification checks behaviour only |
| normal (default) | ordinary features | the final verification also reads the code |
| careful | shared code, data models, public interfaces | design first and weigh a second shape; verify every ticket; run `shilaycow-blast-radius` before the pull request |

### 6.4 Large systems: a chain of tasks

One pull request for a whole system would be too large to review. Large work becomes a chain of tasks, and **the first task's deliverable is the specification itself**:

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Segoe UI, sans-serif","fontSize":"14px","lineColor":"#6B7280","primaryTextColor":"#111827","edgeLabelBackground":"#FFFFFF","clusterBkg":"transparent"},"flowchart":{"curve":"basis","nodeSpacing":40,"rankSpacing":45,"subGraphTitleMargin":{"top":6,"bottom":22}}}}%%
flowchart LR
    T0["<b>Task 0</b><br/><small>explore + spec<br/>documents only</small>"] --> T1["<b>Task 1</b><br/><small>first usable slice</small>"] --> T2["<b>Task 2</b><br/><small>next slice</small>"] --> TN["…"]
    T0 -. "scenarios under Not yet built" .-> SPEC[("<b>docs/spec/</b>")]
    T1 -. "moves its scenarios to Scenarios" .-> SPEC
    T2 -. "moves its scenarios to Scenarios" .-> SPEC

    classDef you fill:#FFF4DB,stroke:#C98A00,stroke-width:1.5px,color:#3D2B00
    classDef agent fill:#E6F0FF,stroke:#2F6FDB,stroke-width:1.5px,color:#0B2552
    classDef gh fill:#E3F6E8,stroke:#2E8B57,stroke-width:1.5px,color:#0D3B22
    classDef gate fill:#FFFFFF,stroke:#C98A00,stroke-width:2px,color:#3D2B00
    classDef stop fill:#FDECEC,stroke:#C0392B,stroke-width:1.5px,color:#5A1410
    classDef neutral fill:#F1F3F6,stroke:#8A94A6,stroke-width:1.5px,color:#1F2633
    class T0,T1,T2,TN agent
    class SPEC gh
```

Each task still merges once, and the spec lands in `main` independently: even if a later task is thrown away, the spec stays.

---

## 7. Verification: how a verdict is reached

`shilaycow-verify` runs in a session that built none of the work, on a clean checkout of one head commit. It treats the builder's claims as claims, not evidence.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Segoe UI, sans-serif","fontSize":"14px","lineColor":"#6B7280","primaryTextColor":"#111827","edgeLabelBackground":"#FFFFFF","clusterBkg":"transparent"},"flowchart":{"curve":"basis","nodeSpacing":40,"rankSpacing":45,"subGraphTitleMargin":{"top":6,"bottom":22}}}}%%
flowchart TD
    S["<b>Clean checkout</b><br/><small>of the head commit</small>"] --> C0{{"Did this session<br/>build any of it?"}}
    C0 -->|"yes"| STOP["<b>Stop</b><br/><small>someone else verifies</small>"]
    C0 -->|"no"| C1
    subgraph CHECKS["<b>Six checks</b><br/><small>each with evidence</small>"]
        direction TB
        C1["<b>1 · Tests</b><br/><small>the full suite passes</small>"]
        C2["<b>2 · Scenarios</b><br/><small>each shown by a test or a driven action;<br/>for main, docs/spec/ matches the work</small>"]
        C3["<b>3 · The real thing</b><br/><small>follow how to try it with the try-app skill</small>"]
        C4["<b>4 · Tests that can fail</b><br/><small>break each behaviour, the test must fail;<br/>expected values come from the scenario</small>"]
        C5["<b>5 · What went unsaid</b><br/><small>unmentioned changes; extremes listed as unspecified</small>"]
        C6["<b>6 · The code itself</b><br/><small>read as its maintainer, cite file and line<br/>(skipped at care level fast)</small>"]
        C1 --> C2 --> C3 --> C4 --> C5 --> C6
    end
    C6 --> J{{"Any FAIL condition?"}}
    J -->|"yes"| F["<b>Verification: FAIL</b><br/><small>which check · how to reproduce · what was seen</small>"]
    J -->|"no"| P["<b>Verification: PASS</b><br/><small>plus Findings for everything else</small>"]

    classDef you fill:#FFF4DB,stroke:#C98A00,stroke-width:1.5px,color:#3D2B00
    classDef agent fill:#E6F0FF,stroke:#2F6FDB,stroke-width:1.5px,color:#0B2552
    classDef gh fill:#E3F6E8,stroke:#2E8B57,stroke-width:1.5px,color:#0D3B22
    classDef gate fill:#FFFFFF,stroke:#C98A00,stroke-width:2px,color:#3D2B00
    classDef stop fill:#FDECEC,stroke:#C0392B,stroke-width:1.5px,color:#5A1410
    classDef neutral fill:#F1F3F6,stroke:#8A94A6,stroke-width:1.5px,color:#1F2633
    class S neutral
    class C0,J gate
    class STOP,F stop
    class C1,C2,C3,C4,C5,C6 agent
    class P gh
    style CHECKS fill:#F5F9FF,stroke:#9DBBF0,stroke-dasharray:4 3,color:#1D4A99
```

Rules that make the verdict trustworthy:

- **Evidence is a command and its output, a screenshot, a file and line.** Never a sentence.
- **One verdict per head commit.** A new commit needs a new verdict, and nothing is pushed after the verdict on the pull request you merge.
- **A finding never turns a PASS into a FAIL, and is never left out to keep a PASS clean.**
- **No behaviour ships on a test that cannot fail.** This is the only rule in the method layer that is enforced.

---

## 8. When the agent stops and asks

In every other situation the agent writes down its assumption (`shilaycow-trail`) and carries on. It stops only when:

| Situation | What it does |
|---|---|
| It needs anything from the boundary table: settings, workflows, secrets, a deploy, an external or paid call | opens an issue labelled `needs-owner` with the options and its recommendation, and continues with whatever that does not block |
| A credential or permission is missing | says what is missing |
| The same failure survives `fix_rounds` rounds | stops and reports |
| The budget (hours or sessions) is used up | stops and reports |
| A scenario cannot be met | opens no pull request into `main`; writes down what is missing |
| You write "stop" on the tracking issue from your own account | ends the run |

---

## 9. Learning: guards that grow from real mistakes

A new project starts with the server-side boundary and nothing else. Guards are added one rung at a time, only after a mistake has actually happened.

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Segoe UI, sans-serif","fontSize":"14px","lineColor":"#6B7280","primaryTextColor":"#111827","edgeLabelBackground":"#FFFFFF","clusterBkg":"transparent"},"flowchart":{"curve":"basis","nodeSpacing":40,"rankSpacing":45,"subGraphTitleMargin":{"top":6,"bottom":22}}}}%%
flowchart TD
    E["<b>A task finishes</b>"] --> R["<b>shilaycow-retro</b><br/><small>FAIL verdicts, fix rounds,<br/>your corrections and comments after merging</small>"]
    R --> PF[("<b>.shilaycow/pitfalls.md</b><br/><small>folded in by the next Chief,<br/>read by every builder</small>")]
    PF --> Q{{"Same class of mistake<br/>happened twice?"}}
    Q -->|"no"| NEXT["<b>Next task avoids it</b>"]
    Q -->|"yes"| COR["<b>shilaycow-correct</b><br/><small>the highest rung that works</small>"]
    subgraph LADDER["<b>The ladder</b><br/><small>highest rung first</small>"]
        direction LR
        L1["<b>1 · Architecture</b><br/><small>the wrong way no longer exists</small>"]
        L2["<b>2 · Types</b><br/><small>the bad state cannot be written</small>"]
        L3["<b>3 · Lint</b><br/><small>the error names the fix</small>"]
        L4["<b>4 · Test</b>"]
        L5["<b>5 · Docs</b><br/><small>last</small>"]
        L1 ~~~ L2 ~~~ L3 ~~~ L4 ~~~ L5
    end
    COR --> LADDER
    LADDER --> PRC["<b>A pull request you merge</b><br/><small>a CI change is a proposal you apply</small>"]
    PRC --> DEL["<b>Pitfall removed</b><br/><small>once the guard catches every past instance</small>"]

    classDef you fill:#FFF4DB,stroke:#C98A00,stroke-width:1.5px,color:#3D2B00
    classDef agent fill:#E6F0FF,stroke:#2F6FDB,stroke-width:1.5px,color:#0B2552
    classDef gh fill:#E3F6E8,stroke:#2E8B57,stroke-width:1.5px,color:#0D3B22
    classDef gate fill:#FFFFFF,stroke:#C98A00,stroke-width:2px,color:#3D2B00
    classDef stop fill:#FDECEC,stroke:#C0392B,stroke-width:1.5px,color:#5A1410
    classDef neutral fill:#F1F3F6,stroke:#8A94A6,stroke-width:1.5px,color:#1F2633
    class E neutral
    class R,COR,NEXT,L1,L2,L3,L4,L5 agent
    class PF,PRC,DEL gh
    class Q gate
    style LADDER fill:#F5F9FF,stroke:#9DBBF0,stroke-dasharray:4 3,color:#1D4A99
```

What you find wrong after merging is the most valuable input: it is what verification missed. One comment on the finished tracking issue is enough; the next task reads it first.

---

## 10. What appears in your repository

```text
.shilaycow/
  config.yml            settings (below)
  pitfalls.md           mistakes this project has made; builders read it first
.claude/skills/
  try-<app>/            how to start and drive your app, made by shilaycow-try-it
docs/spec/
  index.md              what the system is, its areas, its terms, what it does not do
  <area>.md             the scenarios and rules true in that area today
docs/tasks/<slug>/
  brief.md              goal, out of scope, scenarios, how to try, budget, care level, assumptions
  design.md             the design, when the task needs one
  plan.md               milestones and tickets
  tickets/T-<nn>.md     one per ticket
  trail.tsv             every decision made in place of asking
  evidence/             recordings and outputs
  reports/m<n>.md       checkpoint report per milestone
  reports/final.md      final report, also the description of the pull request into main
AGENTS.md               gains a section pointing at .shilaycow/ and the branch names
```

Only two files have a fixed shape, because you read them: `brief.md` (what you approve) and the final report (what you read before merging). Everything else is "usually here, usually like this".

**Who writes and reads what**

| File | Written by | Read by |
|---|---|---|
| `config.yml` | `shilaycow-setup`, then only you | every skill |
| `pitfalls.md` | the next Chief (from `Retro:` comments), `shilaycow-correct` | `shilaycow-plan`, builders |
| `try-<app>` | `shilaycow-try-it`, during the first task | `shilaycow-verify`, `shilaycow-report` |
| `docs/spec/` | `shilaycow-spec`, before each task's pull request | `shilaycow-sharpen`, `shilaycow-verify`, `shilaycow-how`, builders |
| `brief.md` | `shilaycow-sharpen` | design, plan, verify, report |
| `design.md` | `shilaycow-design` | plan, builders, verify |
| `plan.md`, `tickets/` | `shilaycow-plan` | the Chief, builders, verify |
| `trail.tsv` | the Chief, builders | report, verify, retro, you |
| `reports/` | `shilaycow-report` | you |

**Branches**

| Branch | Purpose |
|---|---|
| `main` | delivered work; only you merge |
| `task/<slug>` | the task's integration branch (Levels 3 and 4); `docs/tasks/<slug>/` lives here |
| `work/<slug>/T-<nn>` | one ticket's work |
| `spike/<topic>` | a throwaway prototype; never merged, only its decisions come back |

**The config**

```yaml
# .shilaycow/config.yml
owner: example-owner
bot: example-bot              # may be empty at Level 1
merge_unit: task              # change | ticket | milestone | task  (Level 1 to 4)
test_command: ""              # your test command, if any
budget:
  hours: 8
  sessions: 20
parallel_builders: 2
fix_rounds: 2
report_language: en           # briefs and reports; headings stay in English
```

With no config, every skill behaves as Level 1. The copy on `main` is the one that counts; you can name another level when starting a task, and a task's level is fixed once it starts.

---

## 11. Where state lives, and how a run resumes

Nothing important lives in a conversation. Conversations are compressed and sessions end; a decision that exists only in a chat is treated as never made.

| State | Lives in |
|---|---|
| What was agreed | `brief.md`, `design.md` on the task branch |
| Progress, level, budget | the tracking issue `Task: <slug>`: its first line, then one line each time something lands or waits |
| Decisions made without asking | `trail.tsv` |
| Readiness and verdicts | `Ready.` and `Verification:` comments on pull requests, each tied to a head commit and a `Session:` |
| Questions for you | issues labelled `needs-owner` |

Because of this, starting `shilaycow-chief` again on the same task resumes it: the Chief rebuilds its picture from the repository and GitHub every time. `shilaycow-status` reads the same sources to tell you, without changing anything, what the task is waiting on and what to do next.

---

## 12. When it breaks, and how to recover

| Situation | Consequence | What limits it |
|---|---|---|
| The final pull request is large and you do not read it closely | a problem reaches `main` | the verifier drives every scenario; the report lists every decision the agent made on its own; your test command can be a required check |
| The cloud session is connected to your account, not the bot | the agent acts as you and the ruleset does not apply to it | the Chief checks its GitHub identity before any unattended work and stops if it is not the configured bot |
| Permission prompts are turned off at Level 1 | same as above | documented; cannot be detected |
| The project gains production, real users or secrets | the boundary table is no longer enough | out of scope; `shilaycow-setup` warns when it sees deploy configuration or secrets |
| Builder and verifier are the same model on the same account | verification catches honest mistakes only | accepted: the agent is assumed to cooperate and err, not to cheat; you are the final gate |
| Parallel builders edit the same file | merge conflicts | the Chief runs in parallel only tickets whose areas do not overlap |
| `main` changes during a task | the final pull request conflicts | the Chief merges `main` into the task branch; the conflict happens on a branch you can throw away |
| Tests are written to match the code instead of the scenario | wrong behaviour is locked in as correct | expected values must come from scenarios; the verifier breaks each behaviour; repeats become a grown guard |
| Too much process for a small task | the process constrains the model | depth scales with the task; the Chief says what it skipped |

**Worst cases and how to undo them**

- **A bad task was merged:** press Revert on its pull request. A task is one merge commit, so undoing it is one action.
- **A task went wrong before merging:** close the pull request and delete the task branch. `main` never changed.
- Both rely on the project having no production database or deployment, which is why that is out of scope.
