---
title: "How do autonomous ships avoid collisions? A guide to the research"
date: 2026-11-09
description: "A 2021 review goes through 48 studies of automatic collision avoidance and asks how well the methods cover the collision regulations."
translationKey: "forskning-burmeister-2021"
kilde: "Burmeister and Constapel (2021), CC BY"
---
*Summary of an open-access article. Written by Captain PhD, 9 November 2026.*

## In brief
If ships are to be steered fully or partly by computers, they must be able to follow the collision regulations (COLREG). Two researchers at the Fraunhofer Center for Maritime Logistics and Services in Hamburg have reviewed the research on this. Their conclusion is that many methods work in simple encounters, but none covers the rules in full, and there is no common way of testing them.

## The question
In practice the article asks three things. Which methods for collision avoidance and path planning have been developed in recent years? How well do they cover the collision regulations, especially Part B (steering and sailing rules)? And how close are they to industrial use?

## How it was done
This is a literature review, not a new experiment. The authors searched Google Scholar and ResearchGate and followed references from promising papers. They looked only at English-language, openly accessible work from 2015 to 2020 that deals with the decision of what the ship should do. About 150 works (papers and theses) were examined. After reading abstracts and conclusions, they kept 48. Each work was reviewed by one author and cross-checked by the other, and the results were sorted into fixed categories: algorithm, validation, operating area, what the system outputs, which sensors it needs and how much of the rules it covers.

## What did they find?
- **Methods.** The closest point of approach (CPA) is the most common trigger for avoiding another vessel. Model predictive control appears in most of the works. Deep reinforcement learning is growing but still uncommon. Potential fields, fuzzy logic, genetic algorithms and other methods also appear.
- **Validation.** There is no common, internationally agreed way to test. Most tested in their own simulators. Few used commercial ship simulators or tried the method at sea.
- **Where they work.** Most methods are made for open sea and coastal waters. Few deal with traffic separation schemes or narrow channels.
- **Data.** AIS and radar are the most common data sources. Weather and sea state appear in fewer than one work in five. Visibility, which decides which rules apply, is rarely taken into account.
- **Rules.** Most works address only overtaking, head-on and crossing situations, with the related give-way and stand-on duties. Only one work (Kufoalor and co-authors, 2020) covers nearly all of Part B. Part C (lights and shapes) and Part D (sound and light signals) are in practice not addressed.

## Limitations
The authors point out several themselves. The search covers only two search engines and only open, English-language work from 2015 to 2020. Industry press releases were left out because they seldom show how the algorithms work. Many of the works had no thorough evaluation, so the authors cannot recommend a particular algorithm. Nor do they judge whether a method meets the rules legally. They only note whether a work addresses a given rule.

## What does it mean for seafarers?
This is our own reading, not the article's.
- The rules that are hardest for automation are those that call for judgement: restricted visibility (Rule 19), narrow channels and traffic separation. There the seafarer's judgement still decides.
- That Parts C and D are almost uncovered shows how much a person reads from lights, shapes and sound signals. You can practise exactly this in the games [Lights and shapes](/lanterner/?lang=en) and [Sound signals](/lydsignaler/?lang=en).
- If you are judging a system that promises "COLREG-compliant" collision avoidance, the first question is which rules it has actually been tested against, in which waters and in what visibility.

## Source
Burmeister, H.-C. and Constapel, M. (2021). Autonomous Collision Avoidance at Sea: A Survey. *Frontiers in Robotics and AI*, 8, article 739013. DOI: [10.3389/frobt.2021.739013](https://doi.org/10.3389/frobt.2021.739013). Open access under the [CC BY](https://creativecommons.org/licenses/by/4.0/) licence. The article is also available on [PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC8481591).

*This summary is a pointer and does not replace reading the article. All statements about the content come from the article; the section "What does it mean for seafarers?" is our own assessment.*
