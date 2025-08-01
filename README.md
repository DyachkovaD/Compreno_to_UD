# Compreno_to_UD
A Russian tagset for UD
Updated: 20 Jan 2023
Based on UD guidelines

Parts of speech (Части речи)
Compreno	UD	Конвертация	Примеры
Noun	NOUN		
PROPN	
'Proper' в тегах
lemma = 'бен', 'аль', 'де' + pos=Prefixoid
lemma = ‘#Acronym’ + pos=Invariable
бен Ладен, де Голь
А300, М1
Adjective	ADJ	
pos=’Numeral’ + ‘MaximallyRestrictiveModifiers’=’Ordinal’
label=’OrderInTimeAndSpace’ + semrel="#number:#number:DIGITAL_NUMBER"’’
semrel='"#day_number:DAY_NUMBER"'
IV, третьего
в 1998 году
8 марта
Verb	VERB		
AUX	‘SyntacticParadigm’ = ‘SyntAuxVerb’	
Adverb	ADV		
Number	NUM		
Particle	PART		
Preposition	ADP		
Predicative	ADV		
Interjection	INTJ		
Preposition	ADP		
Pronoun	PRON		
DET	
dep=’det and’ lemma={'такой', 'какой', 'всякий', 'некоторый', 'никакой', 'некий', 'сей', 'чей', 'какой-либо', 'какой-нибудь','кое-какой', 'весь', 'этот', 'тот', 'каждый', 'мой', 'твой', 'ваш', 'наш', 'свой', 'любой', 'каждый', 'какой-то', 'некоторый', 'такой-то', 'чей-то', 'чей-либо', 'кой', 'никой'}
token=lemma / token=’ее’, lemma=’её’
-	SYM	token={'%', '$', '№', '°', '€', '+', '=', '№', '#', '@', '~', '^', '&', '\\','/', '&'}	
Conjunction	CCONJ	‘Coordinator’ в тегах	
SCONJ	иначе	
Grammatical features (FEAT)
Теги adj_feats = ('Case', 'Gender', 'Number', 'DegreeOfComparison')
        + Animacy если Case = Acc, Gender = Masc / Case = Acc, lemma в ('оба', 'обе', 'два', 'три', 'четыре' / Case = Acc, Gender, lemma = 'один');
        - ‘Case’ если Variant = Short;
adv_feats = 'DegreeOfComparison';
noun_feats = ('Animatedness', 'Case', 'Gender', 'Number');
num_feats = ('Animatedness', 'Case', 'Gender');
        - ‘Gender’ если lemma не в ('i', 'ii', 'оба', 'один', 'полтора', 'два');
verb_feats = ('Aspect', 'Mood', 'Number', 'Person', 'Tense', 'GrammaticalType', 'Voice', 'Gender');
        + ‘Case’ если VerbForm = Part, Variant != Short;
pron_feats = ('Animatedness', 'Case', 'Gender', 'Number', 'Person');
det_set = {'Animatedness', 'Case', 'Degree', 'Gender', 'Number'}.

Compreno	UD	Конвертация
Case
Accusative	Acc	
Dative	Dat	
Genitive	Gen	
Genitive|Partitive	
Instrumental	Ins	
Locative	Loc	
Prepositional	
Nominative	Nom	
Partitive	Par	
Vocative	Voc	
ZeroCase	-	
Person
PersonFirst	1	
PersonSecond	2	
PersonThird	3	
PersonZero	-	
DegreeOfComparison	Degree
DegreeSuperlative	Sup	
DegreePositive	Pos	
DegreeComparative	Cmp	
Mood
Imperative	Imp	
Subjunctive	Cnd	
Ind	не Imp, Cnd, NoMood
NoMood	-	
GrammaticalType	VerbForm
GTInfinitive	Inf	
GTVerb	Fin	
GTParticipleAttributive	Part	
GTParticiple	
GTAdverb	Conv	
Animatedness	Animacy
Animate	Anim	
Inanimate	Inan	
Gender
Feminine	Fem	‘SyntacticGender’=’SyntFeminine’
Neuter	Neut	‘SyntacticGender’= ’SyntNeuter’
Masculine	Masc	
Common	-	
Number
Plural	Plur	
Singular	Sing	
Aspect
Perfective	Perf	
Imperfective	Imp	
Если ‘Pairness’=’BiAspectual’ аспекта нет
Tense
Present	Pres	
Future	Fut	‘Tense’=’Pres’ and ‘Aspect’=’Perf’
Past	Past	
Voice
Active	Act	‘Voise’=’VoiceSya’ and ‘SyntActive’ in feats
Passive	Pass	‘Voise’=’VoiceSya’ and ‘SyntPassive’ in feats
VoiceSya	Mid	
