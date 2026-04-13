<!-- keywords: Persian, Farsi, RAG, Language Learning  -->
# **Learning to Read My Father Tongue**

Languages don't die suddenly. They fade. First the writing disappears, then the reading, and eventually even the speaking becomes something that only happens at family dinners, until the generation that remembers those dinners is gone too.

For second-generation Iranians in the diaspora, this is not an abstract concern. Research on heritage language retention consistently shows that while many second-generation immigrants hold onto conversational Farsi, literacy (reading and writing the script) is on a much steeper decline. Studies on Iranian diaspora communities, particularly in the United States, suggest that literate Farsi rarely survives past the second generation. The spoken word hangs on longer, passed down through daily life and family. But the written word, with no school to teach it and no daily necessity to use it, quietly disappears.

I suppose I could say I am also part of that statistic…

Born in the Netherlands to Iranian parents, I can hold a conversation in Farsi, understand the jokes, follow along when my parents talk. But hand me something written in Persian script and I'm lost. I recognize the letters the way you might recognize a face you've seen somewhere but can't quite place. 

For a long time I told myself it didn't matter. I live here, I work in English and Dutch, Farsi is just something that happens at home. But somewhere in the back of my head, that reasoning never quite stuck. Because language is not just a communication tool. It's the thing that connects you to poetry written a thousand years ago, to the handwriting in your parents’ letters, to a culture that is yours even if you inherited it at a distance.

That quiet discomfort eventually turned into a project.

## **The Gap Nobody Talks About**

If you're a heritage speaker, meaning someone who grew up with a language at home without formally learning it, you exist in a strange in-between space. You're not a beginner. You already know the sounds, the grammar patterns, the rhythm of the language. But you're also not literate in the traditional sense, because nobody ever sat you down and taught you to read.

Most language learning resources don't know what to do with you. Duolingo treats you like a complete beginner and makes you translate "the cat drinks milk" for the tenth time. Traditional textbooks assume you know none of the vocabulary. YouTube courses spend thirty minutes explaining sounds you already know how to make.

And Duolingo doesn't even have Farsi, for one of the world's most spoken languages…

So I started looking for resources. What I found was mostly scanned PDFs of 1970s textbooks, paywalled courses, and content aimed at complete beginners with zero spoken background. Not exactly ideal.

## **The Side Project**

Around the same time, I was exploring RAG pipelines (Retrieval-Augmented Generation), a technique where you give an AI model access to a curated knowledge base so it can answer questions grounded in specific documents rather than hallucinating from its training data. I'd been wanting to build something with it for a while.

The two ideas collided. What if I built a Farsi learning app specifically for heritage speakers? One that acknowledges you already speak the language and just helps you bridge the gap to the written form?

So I started building one.

The first challenge was sourcing good materials. Most serious Farsi textbooks are scanned images, which are useless for a RAG pipeline because you can't extract the text (unless you use an Optical Character Recognition algorithm for extracting the text, which is complicated for the farsi script). After a lot of searching I found a few digitally-born resources: *Persian of Iran Today* by Shahsavari and Atwood, the Routledge Intermediate Persian Course, and a PersianPod101 alphabet worksheet. I also generated a custom 2000+ word vocabulary list (thank you Claude) specifically structured for heritage learners, flagging words with dual meanings, and including cultural context that a generic dictionary would miss.

The tech stack: Python backend with FastAPI for the RAG pipeline using LangChain, and a Next.js \+ TypeScript frontend — new territory for me coming from Flask. The shift from server-rendered HTML templates to component-based React was a genuine mental model change. Worth it, but humbling.

## **What I Actually Learned**

Building this taught me something I didn't expect: the process of sourcing, cleaning, and structuring knowledge for a RAG system is genuinely hard. It's not just throwing PDFs at a vector database and hoping for the best. You have to think about chunk size, metadata, the quality of each source, whether the text is even extractable. Two out of three textbooks I found were scanned images, and thus completely unusable without OCR.

The quality of a RAG system lives and dies by the quality of its knowledge base. That's the part that takes real judgment, not just technical skill.

I also learned that there's a meaningful difference between building something because it's technically interesting and building something you personally need. The Farsi app sits in both categories, which made the decisions — what to include, how to structure the experience, what a heritage speaker actually needs — feel obvious rather than arbitrary.

## **The Honest Take**

Is this going to become a subscription product? Probably not. The audience is niche, the marketing challenge is real. But as a portfolio project that taught me RAG architecture, a modern TypeScript frontend, and end-to-end system design, it was absolutely worth building.

And on a more personal level: I'm actually learning to read Farsi now. Slowly. My parents are my fact-checkers for the vocabulary lists, which has led to some unexpectedly good conversations about words, their origins, and the gap between what's written and what's actually said.
