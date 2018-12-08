# The Echo Chamber Effect - A Case Study (provisional title)

## Abstract
Has the high connectivity that came with the internet made us better? Is it fostering healthy discussion and debate between the different communities or is the amount of information available distracting us from the real issues of our society? Which sources are reliable? Who to trust? If we form an opinion, was it really our own or were we influenced by someone with an agenda? Do this things even happen or is this all just tin-foil hat speculation?

Questions like this arise in our day-to-day interactions with modern social media but answering them requires a tremendous amount of effort due to the sheer amount of data at our fingertips. To have a good picture of how a particular technology (the internet no less) is shaping debate we need metrics. The focus of this project is one of the main arguments presented against modern mass social media: the so called echo chamber effect ( https://en.wikipedia.org/wiki/Echo_chamber_(media) ). We will try, from a naive data centric perspective (unfortunately, we are NOT social sciences experts), to understand this phenomenon, describe it, and hopefully come up a tangible metric or benchmark that serves a simple purpose: determining if a certain community constitutes an echo chamber and/or to what degree.

We believe that this is really important since big challenges lie ahead of our generation: climate change, the rise of populism or the increasing inequality, both between nations and inside their borders, just to give a few examples. Fake news and crafted narratives have been a hot topic for a while, and while the internet has given certain agents the ability to reach a lot of people with minimal effort it has also provided huge advancements just for the mere fact that sharing information and knowledge is easier than ever in history. Hence, understanding the way in which we communicate through that vast network is key in order to come up with ways to protect ourselves from bad actors that might try to influence our reasoning.

## Research questions
- What is the echo-chamber effect? Can we really measure it? If so, how?  
- Does it have a stronger effect on certain topics? What factors influence it?  
- Is the echo chamber effect present in all of Reddit or can it be narrowed down to some communities?

## The roadmap
Now that we are acquainted with the dataset we can say that, while a difficult task, our plan of attack should be as follows:
- Develop more stats and ways to visualize the dataset and, in particular, subreddits
- Use NLP to analyse and classify the contents of the comments
- After those systems are in place, look at the biggest cases of echo chambering and perform inference
- Create a heuristic, or several, designed to fit the echo chambers that we found during the analysis.
- Test our heuristics upon the rest of the communities and see if they perform well and if they allow us to find other echo chambers
- Draw conclusions

## What is Reddit?
Reddit is the "frontpage of the internet" (13 years online, more than half a billion monthly users, top 3 most visited website in the US and top 20 in the world). According to [Wikipedia](https://en.wikipedia.org/wiki/Reddit) Reddit is "an American social news aggregation, web content rating, and discussion website". What does this mean? There are two main elements to Reddit:

- The communities of Reddit are called **subreddits**. They are easily identified by a preceding 'r/' (e.g. [r/datascience](https://www.reddit.com/r/datascience/)). These communities are created and managed entirely by their users. One can think of them as topics. [r/gaming](https://www.reddit.com/r/gaming/) is the place you go for anything related to games, while [r/catpictures](https://www.reddit.com/r/catpictures/) is for... well, cat pictures. A subreddit is a place where information about a certain topic is posted, curated, discussed and memed upon by all its users. And here is where the most important and defining part or Reddit comes up...

- The **voting system**. Reddit has a very simple system (yet with complex ramifications, as we are about to discover) to know what information is relevant. After a post (usually a link to an article on the web, a picture, a question, or just an opinion on something) is submitted to a particular (fitting) subreddit users are allowed to both comment on it and either upvote or downvote the post. Posts with a higher score (upvotes - downvotes) are assumed to be of most relevance to the community and thus will remain higher on the subreddit's feed. Similarly, the comments under that post can also be voted on, the top comment being the one with a higher score. If your content gets upvotes you get karma, a.k.a. Internet Points. They are worth... nothing. Yet this is an effective way in which the system rewards your contributions. They serve as both a reputation metric and a legacy reminding you that you were useful to the community.

As you can see, there is no complicated algorithm ala Facebook to determine relevance, no personalized AI-powered feeds Twitter-style, no Amazon recommenders telling you what to read based on your observed preferences. You want to see dogs, you go to [r/dogs](https://www.reddit.com/r/dogs/), plain and simple. The catch? People vote on what's relevant so if a majority are wrong, biased, or someone with the means gets enough people to believe something, then that something becomes the truth. The voting system is both the greatest advantage and the single point of failure of Reddit.

Reddit's developers are open about the huge amount of information that flows around the site and the responsibility it takes to handle such a social and news outlet (e.g. [yearly summaries](https://redditblog.com/2018/12/04/reddit-year-in-review-2018/), [transparency reports](https://www.reddit.com/wiki/transparency), [engagement in politics](https://redditblog.com/2018/10/17/politics-on-reddit/)). They are very open to the community, value neutrality and seem to work to keep the system clean of bad actors that try to game it. For this project we will make use of the dataset containing all of the comments posted to Reddit since it's inception in 2005 and until March 2017, which should make up for a pretty good (mainly, more on that later) uncensored dataset on the interaction between and within different communities. In particular, since the size of the data is too much for a bunch of students, even with the power of EPFL's IC Cluster, we will restrict ourselves to the entirety of 2016 and the first 3 months of 2017.

## So, what is an echo chamber?
We call a community an echo chamber when, due to either external factors or by design, a community that shows built-in biases, traits, opinions, etc interacts (relatively) only within itself, self-reinforcing those opinions and biases.

### Why is it bad?
Echo chambers are as old as communities themselves. We need to understand that this is not a new thing. Before the internet, neighbourhoods, family cores and friendship circles were also echo chambers. An echo chamber on an uninformed community can create its own beliefs, its own realities, leading to tribalism ("you don't belong to my group, why should I trust you over them?"). The internet and mass social media only escalated the phenomenon to epic proportions. Due to the insulating nature of echo chambers, other dangerous phenomena that occur naturally in social interaction networks (not only on the internet) get amplified. See [communal reinforcement](https://en.wikipedia.org/wiki/Communal_reinforcement), [confirmation bias](https://en.wikipedia.org/wiki/Confirmation_bias), [missinformation](https://en.wikipedia.org/wiki/Misinformation) and [disinformation](https://en.wikipedia.org/wiki/Disinformation), [filter bubbles](https://en.wikipedia.org/wiki/Filter_bubble), [groupthinking](https://en.wikipedia.org/wiki/Groupthink), or [false consensus](https://en.wikipedia.org/wiki/False_consensus_effect) just to name a few.

Another of the problems facing echo chambers is exploitability. In an era where [hypertargeting](https://en.wikipedia.org/wiki/Hypertargeting) is increasingly one of the most profitable forms of marketing it is very easy to go dark and imagine a group with an agenda targeting a certain community. If an online community constitutes a strong echo chamber the task of identifying and targeting its users becomes that much easier. Again, this is not new, news outlets have used this since forever to push certain political ideas. But today a company like Cambridge Analytica can target a community's users across the web and all major social media platforms and craft information bubbles around us.

Imagine the following situation: A PC user wants to decide on a brand to buy their new graphics card. As soon as they make a couple of google searches they will be targeted with adds from a company. This is out of their control, they will be spammed no matter what with taylored information to convince them of something. Now if the user conducts his research and explores multiple sources for their information they are likely to ultimately be able to make a much more informed choice. If, on the contrary, their main source of information comes from an echo chamber (like a subreddit for NVIDIA fans) they are then likely to see those ideas that are being fed through adds reinforced, not even aware of the alternatives that are at hand. This also creates a feedback loop where by being part of such a community he is more likely to be on the receiving end of adds by NVIDIA and as they become more polarized the competition will soon give up on trying to convince them, switching efforts to another more psychologically predisposed customer.

Our understanding of this phenomenon is still building up and hopefully the articles and examples below will help greatly explain what an echo chamber looks like.

- Article about echo chambers in [the conversation](http://theconversation.com/how-to-check-if-youre-in-a-news-echo-chamber-and-what-to-do-about-it-69999).  
- Another article in [Scientific American](https://blogs.scientificamerican.com/a-blog-around-the-clock/web-breaks-echo-chambers-or-echo-chamber-is-just-a-derogatory-term-for-community/).  
- [Echo chambers during Brexit](https://arxiv.org/ftp/arxiv/papers/1709/1709.05233.pdf) (relating online communities to socioeconomic data).  
- A similar [project](https://dsi.virginia.edu/projects/echo-chambers-audience-and-community).

### Some examples of echo chambers
The following subreddits share one trait: dissent is not allowed within them.  
They are the prime example of an echo chamber. Several of them support hate speech, antisemitism and/or extremist views, as is usual with echo chambers. They are the main argument against modern social media as we know it: platforms like Reddit allow their users to confine themselves to this curated spaces where expressing certain points of view while heavily censoring others is not only regarded as normal but also encouraged as etiquette.

- [r/ShitRedditSays](https://www.reddit.com/r/ShitRedditSays/) is a sub with a golden rule in place: "Do not defend linked comments. Do not play Devil's Advocate. Do not attempt to start a debate."
- [r/Braincels](https://www.reddit.com/r/Braincels/) the term incel stands for "involuntary celibate". This community is tied by a real, tangible condition. Outsiders are rapidly identified, downvoted and harassed until they leave. This is known to be a pretty aggressive community towards women and a hub for misogyny and it is currently [quarantined](https://www.reddithelp.com/en/categories/rules-reporting/account-and-community-restrictions/quarantined-subreddits) by Reddit, meaning that a warning for highly offensive content is displayed before one can browse the sub.
- [r/the_donald](https://www.reddit.com/r/the_donald) is a sub where only Trump supporters are allowed. Criticism is not permitted as a rule. Even honest questions about Trump are redirected to another sub. It is engineered to praise his figure with no outsider input.

These are some examples selected not because of their particular content but because it is so easy to find signs of echo chambering within them. Most of this subs have rules in place that prevent anyone to challenge the initial premises upon which the community builds. They usually restrict their userbase (incels(male), Trump supporters) and actively censor content and users through the moderation tools available. The content instantly reflects this: polarizing statements in favor of the premise tend to get high scores in absence of opposition, while critique or views "from the other side" are non-existent.

### Candidates to non echo chamber
An echo chamber doesn't have to be filled with hate speech necessarily, nor does it need to be restricted to a topic (and conversely, not all single-topic subs are echo chambers). It is a place where dissent is not allowed and discussion is silenced (directly or indirectly). To some extent one could say that Reddit as a whole is an echo chamber due to the voting system: "accepted" views rise to the top while "dissenting" opinions are sink to the deeps, but there are degrees to such phenomena:

- [r/itookapicture](https://www.reddit.com/r/itookapicture/) is dedicated to photography. This sub encourages critique seeking and participating in the discussion in its rules.
- [r/politics](https://www.reddit.com/r/politics/) is the main subreddits for US politics discussion. While it has no rules in place banning critique or forcing a bias on its users we need to take into account that Reddit users already have a bias since they are not a random sample of the population. This might after all be an echo chamber.
- More to come...

The main difference between those and the previously listed communities can be appreciated very easily by looking at the rules of those subs (in the sub page, right sidebar for desktop, 'About' tab for mobile). This subs don't filter their userbase (r/twoXchromosomes is about women's perspectives but everyone is allowed to post/comment on it) nor blanket ban certain specific behaviours, users or points of view. Instead the rules provide a generic baseline of etiquette, discussion and formatting guidelines while leaving the content moderation to the upvote system (a.k.a. the users). At a glance, one can see that the content is less polarizing, it is frequent to see people disagree in the comments

### Summary

In short, the main trait of echo chambers seems to be related to introducing a built-in bias, for example via censorship or by carefully selecting who gets a say. A sub about a certain videogame might or might not be an echo chamber, while a sub about *how good* that videogame is with rules in place banning critique or nonfans of the game from posting probably is an echo chamber.

## Dataset
We plan on using the Reddit comments dataset. It contains all of reddit's comments from its inception and up to March 2017. Reddit already has a rich structure and we plan to take advantage of it. We are going to focus on subreddits, as those are going to be our communities. Since we also have user data we can watch for cross-interaction between subreddits, brigading, trolls, bots, etc.
This is basically a list of 53,851,542 JSON objects with comments using the following structure:

{  

   "gilded":0,  
   "author_flair_text":"Male",  
   "author_flair_css_class":"male",  
   "retrieved_on":1425124228,  
   "ups":3,  
   "subreddit_id":"t5_2s30g",  
   "edited":false,  
   "controversiality":0,  
   "parent_id":"t1_cnapn0k",  
   "subreddit":"AskMen",  
   "body":"content",  
   "created_utc":"1420070668",  
   "downs":0,  
   "score":3,  
   "author":"TheDukeofEtown",  
   "archived":false,  
   "distinguished":null,  
   "id":"cnasd6x",  
   "score_hidden":false,  
   "name":"t1_cnasd6x",  
   "link_id":"t3_2qyhmp"  
}

Specifically, we plan to mainly use the username, subreddit id, and timestamp. As the project unfolds we might make use of controversiality, downvotes, score, etc in order to go more in depth (if time allows).

Some speedbumps we might find are dead subreddits and known bots posting useless comments, we might have to work a bit if we want to clean the dataset perfectly but it looks mostly solid. The good thing about reddit is that there's probably about a thousand good resources we can find online for such a task.

Size-wise we might also encounter some roadblocks since this is a pretty big dataset. If we find that it's too much to handle we might resort to shrinking substantially, which thanks to the good structure can be done easily.

## Internal milestones up until project milestone 1
- Decide on the dataset we want to use and a topic
- Write this README and have an idea of what we actually want to do

## Internal milestones up until project milestone 2
- Get the dataset from the cluster (or the subset of the data we are going to use) and filter/sample as necessary
- Understand and explain the structure of the data
- Perform some basic stats on the data, get familiar with it
- Load and try some libraries and tools we could potentially use
- Once the data is in our hands, trace a roadmap to our goals

## Internal milestones up until milestone 3
- Get familiar with the phenomenon of the echo-chamber, find sources and references
- Get a list of potential echo chambers (and non echo chambers as well) in reddit to test our metrics
- Set the foundations of our study using well-known concepts from graph and network theory
- Propose several metrics to measure the effect
- Test the different metrics in particular communities and observe their performance


## Links of Interest
Source code of reddit (python): https://github.com/reddit  
Reddit FAQ: https://www.reddit.com/wiki/faq  
Reddit API: https://www.reddit.com/dev/api/  
Dev post about controversiality: https://www.reddit.com/r/announcements/comments/293oqs/new_reddit_features_controversial_indicator_for/  
Lists of bots in Reddit: https://www.reddit.com/r/botwatch/comments/1xojwh/list_of_320_reddit_bots/  
Some stats about reddit: https://www.similarweb.com/website/reddit.com  
Reddit user analyzer: https://atomiks.github.io/reddit-user-analyser/  
News about social engineering: https://www.reddit.com/r/science/comments/a01xix/a_study_has_found_social_network_bots_actually/  
Other: https://en.wikipedia.org/wiki/Echo_chamber  
