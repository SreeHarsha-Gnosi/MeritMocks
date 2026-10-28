"""IBPS PO Prelims — Free Mock 1. Original questions written for MeritMocks.

Each section is a list of groups. A group with `directions` becomes a Passage
shared by its questions; `answer` is the 0-based index of the correct option.
"""

ERROR_OPTIONS = ['A', 'B', 'C', 'D', 'No error']
PARA_OPTIONS = ['A', 'B', 'C', 'D', 'E']
QUADRATIC_OPTIONS = ['x > y', 'x < y', 'x ≥ y', 'x ≤ y', 'x = y or the relationship cannot be established']
SYLLOGISM_OPTIONS = [
    'Only conclusion I follows',
    'Only conclusion II follows',
    'Either conclusion I or II follows',
    'Neither conclusion I nor II follows',
    'Both conclusions I and II follow',
]
INEQUALITY_OPTIONS = [
    'Only conclusion I is true',
    'Only conclusion II is true',
    'Either conclusion I or II is true',
    'Neither conclusion I nor II is true',
    'Both conclusions I and II are true',
]

MOCK = {
    'category': {'name': 'Banking', 'slug': 'banking', 'order': 1,
                 'tagline': 'IBPS, SBI and RRB officer & clerk exams'},
    'exam': {'name': 'IBPS Probationary Officer', 'short_name': 'IBPS PO', 'slug': 'ibps-po',
             'conducting_body': 'Institute of Banking Personnel Selection'},
    'title': 'IBPS PO Prelims · Free Mock 1',
    'slug': 'ibps-po-prelims-free-mock-1',
    'stage': 'Prelims',
}

RC_PASSAGE = """
<p>Over the past decade, India has built one of the most ambitious digital public infrastructures in the world. A unique identity system, near-universal bank accounts and an instant payment network have together brought millions of first-time users into the formal financial system. A street vendor who once relied entirely on cash can now accept payments through a phone, and a farmer can receive a subsidy directly into her account without visiting a government office.</p>
<p>Yet access is not the same as inclusion. Opening an account is a single act; using it meaningfully is a habit that must be <b>nurtured</b>. Surveys continue to find that a significant share of new accounts remain <b>dormant</b>, either because their owners see little reason to keep money in a bank or because they distrust institutions that once ignored them. For such households, a bank account is less a tool than a formality.</p>
<p>Credit tells a similar story. Small borrowers have historically been excluded not because they were unreliable but because lenders lacked information about them. The digital trail left by everyday payments now offers a remedy: a shopkeeper's steady stream of receipts can serve as evidence of repayment capacity that no paper document ever could. Several lenders have begun to use such data to extend small, short-term loans at a fraction of the cost of traditional appraisal.</p>
<p>This promise carries its own hazards. Algorithms trained on incomplete data may quietly reproduce old prejudices, and borrowers who do not understand the terms of a loan offered in a few taps can slip into debt far more easily than they climbed out of poverty. <b>Aggressive</b> recovery practices adopted by some digital lenders have already drawn the attention of regulators.</p>
<p>The challenge for the next decade, therefore, is not to connect more people but to ensure that connection translates into confidence. Financial literacy, transparent pricing and accessible grievance redressal are as much a part of the infrastructure as servers and software. Technology has opened the door; institutions must now make the room worth entering.</p>
"""

PARA_JUMBLE = """
<p><b>(A)</b> As a result, many of them now carry out routine transactions without ever visiting a branch.</p>
<p><b>(B)</b> In the early years, customers were wary of trusting their savings to a screen.</p>
<p><b>(C)</b> Mobile banking in India has travelled a long way in a short time.</p>
<p><b>(D)</b> Banks responded by simplifying their apps and offering support in regional languages.</p>
<p><b>(E)</b> Over time, however, convenience and these efforts gradually won them over.</p>
"""

PARA_EXPLANATION = (
    'The correct sequence is <b>C B D E A</b>. C introduces the topic; B describes the early '
    'wariness; D shows how banks responded; E ("these efforts") refers back to D; A ("As a '
    'result") gives the outcome.'
)

CLOZE = """
<p>Inflation is often described as a hidden tax because it <b>(24)</b>________ erodes the purchasing power of money without any formal announcement. When prices rise faster than incomes, households are <b>(25)</b>________ to cut back on consumption or draw down their savings. Central banks therefore try to keep inflation within a <b>(26)</b>________ target band. To do this, they <b>(27)</b>________ the policy interest rate: raising it makes borrowing more expensive and cools demand, while lowering it does the <b>(28)</b>________. However, monetary policy works with a <b>(29)</b>________, and its full effect may not be felt for several quarters. This is why central bankers must <b>(30)</b>________ future trends rather than merely react to current data.</p>
"""

DI_TABLE = """
<p>The table shows the number of loan applications received by five banks in 2025, the percentage of those applications that were approved, and the percentage of <i>approved</i> applications that were home loans.</p>
<table class="data-table">
  <thead><tr><th>Bank</th><th>Applications received</th><th>% approved</th><th>% of approved that are home loans</th></tr></thead>
  <tbody>
    <tr><td>A</td><td>1200</td><td>65%</td><td>40%</td></tr>
    <tr><td>B</td><td>1500</td><td>48%</td><td>25%</td></tr>
    <tr><td>C</td><td>900</td><td>80%</td><td>50%</td></tr>
    <tr><td>D</td><td>1600</td><td>55%</td><td>35%</td></tr>
    <tr><td>E</td><td>1000</td><td>72%</td><td>45%</td></tr>
  </tbody>
</table>
"""

DI_WORKING = (
    'Approved = applications × % approved: A 780, B 720, C 720, D 880, E 720. '
    'Home loans = approved × home %: A 312, B 180, C 360, D 308, E 324.'
)

CIRCULAR = """
<p>Eight persons — P, Q, R, S, T, U, V and W — are sitting around a circular table, all facing the centre.</p>
<ul>
  <li>R sits third to the right of Q.</li>
  <li>Only one person sits between Q and S.</li>
  <li>U sits second to the left of S.</li>
  <li>P is an immediate neighbour of both S and U.</li>
  <li>W sits to the immediate right of T.</li>
  <li>V is not an immediate neighbour of T.</li>
</ul>
"""

CIRCULAR_SOLUTION = (
    'Final arrangement (clockwise, everyone facing the centre): '
    '<b>P → U → R → W → T → Q → V → S</b>. For a person facing the centre, left is clockwise.'
)

FLOORS = """
<p>Seven persons — A, B, C, D, E, F and G — live on seven different floors of a building. The lowermost floor is numbered 1 and the topmost floor is numbered 7. Each of them likes a different fruit — Apple, Banana, Cherry, Grapes, Kiwi, Mango and Orange.</p>
<ul>
  <li>B lives on an even-numbered floor. Only two persons live between B and the one who likes Banana.</li>
  <li>The one who likes Banana lives on an odd-numbered floor below B.</li>
  <li>F lives immediately above the one who likes Grapes.</li>
  <li>Only one person lives between F and G. G likes Apple.</li>
  <li>C does not like Banana.</li>
  <li>A lives immediately below D. D lives on a floor above B.</li>
  <li>The one who likes Kiwi lives on the topmost floor.</li>
  <li>The one who likes Mango lives immediately above G.</li>
  <li>The one who likes Orange lives immediately below the one who likes Apple.</li>
  <li>The one who likes Cherry lives on an odd-numbered floor.</li>
</ul>
"""

FLOORS_SOLUTION = (
    '<table class="data-table"><thead><tr><th>Floor</th><th>Person</th><th>Fruit</th></tr></thead><tbody>'
    '<tr><td>7</td><td>D</td><td>Kiwi</td></tr><tr><td>6</td><td>A</td><td>Mango</td></tr>'
    '<tr><td>5</td><td>G</td><td>Apple</td></tr><tr><td>4</td><td>B</td><td>Orange</td></tr>'
    '<tr><td>3</td><td>F</td><td>Cherry</td></tr><tr><td>2</td><td>C</td><td>Grapes</td></tr>'
    '<tr><td>1</td><td>E</td><td>Banana</td></tr></tbody></table>'
)

LINEAR = """
<p>Eight persons — J, K, L, M, N, O, X and Y — are sitting in a straight line, all facing north.</p>
<ul>
  <li>J sits third to the right of L.</li>
  <li>L sits at one of the extreme ends.</li>
  <li>Only two persons sit between J and K.</li>
  <li>M sits to the immediate right of K.</li>
  <li>N sits second to the left of O.</li>
  <li>Y is not an immediate neighbour of J.</li>
  <li>X sits somewhere to the left of N.</li>
</ul>
"""

LINEAR_SOLUTION = 'Final arrangement (left to right): <b>L X N J O Y K M</b>.'

NUMBERS = '<p class="numbers-row">734 &nbsp; 586 &nbsp; 921 &nbsp; 469 &nbsp; 358</p>'


def q(text, options, answer, explanation=''):
    return {'text': text, 'options': options, 'answer': answer, 'explanation': explanation}


SECTIONS = [
    {
        'name': 'English Language',
        'minutes': 20,
        'groups': [
            {
                'topic': 'Reading Comprehension',
                'directions': 'Directions (1–8): Read the following passage carefully and answer the questions given below it. Certain words have been printed in bold to help you locate them while answering some of the questions.',
                'body': RC_PASSAGE,
                'layout': 'split',
                'questions': [
                    q('According to the passage, why were small borrowers historically excluded from formal credit?',
                      ['They had a poor record of repaying loans',
                       'Interest rates on small loans were capped by regulators',
                       'Lenders lacked information to judge their ability to repay',
                       'They preferred to borrow from informal moneylenders',
                       'They did not have bank accounts'],
                      2, 'Paragraph 3: they were excluded "not because they were unreliable but because lenders lacked information about them".'),
                    q('What does the author mean by the statement "access is not the same as inclusion"?',
                      ['Having a bank account does not by itself mean that it is used meaningfully',
                       'Only people with smartphones can be financially included',
                       'Bank branches are still necessary for inclusion',
                       'Government subsidies discourage people from using banks',
                       'Inclusion is impossible without access to credit'],
                      0, 'The next sentences explain that opening an account is a single act, while using it meaningfully is a habit — many new accounts remain dormant.'),
                    q('Which of the following is NOT mentioned in the passage as a risk associated with digital lending?',
                      ['Algorithms reproducing old prejudices',
                       'Borrowers not understanding loan terms',
                       'Aggressive recovery practices',
                       'Cyber-attacks leading to the theft of deposits',
                       'Borrowers slipping into debt easily'],
                      3, 'Paragraph 4 mentions biased algorithms, borrowers not understanding terms and slipping into debt, and aggressive recovery. Cyber-attacks are not mentioned.'),
                    q('Which of the following can be inferred from the passage?',
                      ['Digital lenders charge higher interest than traditional banks',
                       'Records of everyday payments can partly replace paper documents in assessing creditworthiness',
                       'Most new bank accounts in India are actively used',
                       'Regulators have banned digital lending apps',
                       'Financial literacy is less important than technology'],
                      1, 'Paragraph 3: a shopkeeper\'s receipts "can serve as evidence of repayment capacity that no paper document ever could".'),
                    q('Which of the following is the most appropriate title for the passage?',
                      ['The Rise of the Cashless Street Vendor',
                       'Why Digital Lenders Must Be Banned',
                       'From Access to Confidence: The Next Step in Financial Inclusion',
                       'Algorithms and the Future of Banking Jobs',
                       'How Subsidies Reach Farmers'],
                      2, 'The passage moves from the success of access to the need for confidence and meaningful use — captured by this title.'),
                    q('Choose the word which is most similar in meaning to the word <b>DORMANT</b> as used in the passage.',
                      ['Fraudulent', 'Inactive', 'Overdrawn', 'Closed', 'Dangerous'],
                      1, '"Dormant" accounts are those that exist but are not being used — i.e. inactive.'),
                    q('Choose the word which is most similar in meaning to the word <b>NURTURED</b> as used in the passage.',
                      ['Restricted', 'Observed', 'Imposed', 'Ignored', 'Fostered'],
                      4, 'A habit that must be "nurtured" must be encouraged and developed — fostered.'),
                    q('Choose the word which is most opposite in meaning to the word <b>AGGRESSIVE</b> as used in the passage.',
                      ['Forceful', 'Hostile', 'Restrained', 'Eager', 'Sudden'],
                      2, '"Aggressive" means forceful or hostile; its opposite is "restrained".'),
                ],
            },
            {
                'topic': 'Error Spotting',
                'directions': 'Directions (9–13): Read each sentence to find out whether there is any grammatical or idiomatic error in it. The error, if any, will be in one part of the sentence. Mark the letter of that part as your answer. If there is no error, mark "No error".',
                'layout': 'inline',
                'questions': [
                    q('Neither the manager nor his assistants <b>(A)</b> / was present at the meeting <b>(B)</b> / held yesterday to discuss <b>(C)</b> / the quarterly targets. <b>(D)</b>',
                      ERROR_OPTIONS, 1, 'With "neither…nor", the verb agrees with the nearer subject — "assistants" is plural, so "was" should be "were".'),
                    q('The bank has introduced <b>(A)</b> / a new scheme which <b>(B)</b> / will benefit to <b>(C)</b> / small depositors across the country. <b>(D)</b>',
                      ERROR_OPTIONS, 2, '"Benefit" as a verb takes a direct object; remove "to" — "will benefit small depositors".'),
                    q('Hardly had the auditors arrived <b>(A)</b> / when the manager <b>(B)</b> / produced all the records <b>(C)</b> / that they had asked for. <b>(D)</b>',
                      ERROR_OPTIONS, 4, '"Hardly had … when" is the correct construction. The sentence has no error.'),
                    q('One of the most important reason <b>(A)</b> / for the decline in <b>(B)</b> / household savings is the rise <b>(C)</b> / in consumer spending. <b>(D)</b>',
                      ERROR_OPTIONS, 0, '"One of the …" is always followed by a plural noun — "reasons".'),
                    q('If I would have known <b>(A)</b> / about the change in schedule, <b>(B)</b> / I would have informed <b>(C)</b> / all the candidates in advance. <b>(D)</b>',
                      ERROR_OPTIONS, 0, 'In a third conditional, the if-clause uses the past perfect: "If I had known".'),
                ],
            },
            {
                'topic': 'Fill in the Blanks',
                'directions': 'Directions (14–18): Each sentence below has a blank. Choose the word that best fits the meaning of the sentence as a whole.',
                'layout': 'inline',
                'questions': [
                    q('The committee\'s report was so ________ that even its critics praised the clarity of its recommendations.',
                      ['vague', 'lucid', 'obscure', 'verbose', 'tentative'],
                      1, 'The clue is "clarity" — "lucid" means clearly expressed.'),
                    q('Despite repeated reminders, the borrower failed to ________ the loan within the stipulated period.',
                      ['recover', 'sanction', 'disburse', 'repay', 'waive'],
                      3, 'A borrower repays a loan; the bank sanctions, disburses, recovers or waives it.'),
                    q('Welcomed by traders, the new policy is expected to ________ the compliance burden on small businesses.',
                      ['intensify', 'inflate', 'double', 'complicate', 'ease'],
                      4, 'Traders would welcome a policy that reduces, i.e. eases, the burden.'),
                    q('The economist cautioned that the recent surge in prices was not a ________ phenomenon but the start of a lasting trend.',
                      ['transient', 'permanent', 'structural', 'persistent', 'durable'],
                      0, 'The contrast with "lasting trend" requires a word meaning short-lived — "transient".'),
                    q('Her ________ attention to detail made her the ideal candidate to lead the audit team.',
                      ['casual', 'cursory', 'meticulous', 'careless', 'sporadic'],
                      2, 'An auditor needs careful, precise attention — "meticulous".'),
                ],
            },
            {
                'topic': 'Para Jumbles',
                'directions': 'Directions (19–23): Rearrange the following five sentences (A), (B), (C), (D) and (E) in the proper sequence to form a meaningful paragraph and then answer the questions given below.',
                'body': PARA_JUMBLE,
                'layout': 'split',
                'questions': [
                    q('Which of the following should be the <b>FIRST</b> sentence after rearrangement?', PARA_OPTIONS, 2, PARA_EXPLANATION),
                    q('Which of the following should be the <b>SECOND</b> sentence after rearrangement?', PARA_OPTIONS, 1, PARA_EXPLANATION),
                    q('Which of the following should be the <b>THIRD</b> sentence after rearrangement?', PARA_OPTIONS, 3, PARA_EXPLANATION),
                    q('Which of the following should be the <b>FOURTH</b> sentence after rearrangement?', PARA_OPTIONS, 4, PARA_EXPLANATION),
                    q('Which of the following should be the <b>FIFTH (LAST)</b> sentence after rearrangement?', PARA_OPTIONS, 0, PARA_EXPLANATION),
                ],
            },
            {
                'topic': 'Cloze Test',
                'directions': 'Directions (24–30): In the following passage there are blanks, each of which has been numbered. For each blank, choose the word that best fits the meaning of the passage.',
                'body': CLOZE,
                'layout': 'split',
                'questions': [
                    q('Choose the word that best fits blank <b>(24)</b>.',
                      ['loudly', 'openly', 'quietly', 'rarely', 'suddenly'],
                      2, 'A "hidden tax" works without announcement — it "quietly" erodes purchasing power.'),
                    q('Choose the word that best fits blank <b>(25)</b>.',
                      ['forced', 'eager', 'delighted', 'refused', 'hesitant'],
                      0, 'When prices outpace incomes, households have no choice — they are "forced" to cut back.'),
                    q('Choose the word that best fits blank <b>(26)</b>.',
                      ['random', 'predetermined', 'infinite', 'secret', 'fluctuating'],
                      1, 'Central banks target a set, announced range — a "predetermined" band.'),
                    q('Choose the word that best fits blank <b>(27)</b>.',
                      ['ignore', 'abolish', 'conceal', 'adjust', 'freeze'],
                      3, 'The next clause describes raising and lowering the rate — they "adjust" it.'),
                    q('Choose the word that best fits blank <b>(28)</b>.',
                      ['same', 'similar', 'opposite', 'equal', 'least'],
                      2, 'Raising the rate cools demand; lowering it does the "opposite".'),
                    q('Choose the word that best fits blank <b>(29)</b>.',
                      ['haste', 'lag', 'speed', 'rush', 'pause'],
                      1, 'Its effect is not felt for several quarters — policy works with a "lag".'),
                    q('Choose the word that best fits blank <b>(30)</b>.',
                      ['neglect', 'forget', 'dismiss', 'reverse', 'anticipate'],
                      4, 'Because of the lag, bankers must look ahead — "anticipate" future trends.'),
                ],
            },
        ],
    },
    {
        'name': 'Quantitative Aptitude',
        'minutes': 20,
        'groups': [
            {
                'topic': 'Simplification',
                'directions': 'Directions (31–35): What value should come in place of the question mark (?) in the following questions?',
                'layout': 'inline',
                'questions': [
                    q('45% of 640 + 3/8 of 512 − 18² = ?',
                      ['148', '152', '156', '160', '164'],
                      2, '288 + 192 − 324 = <b>156</b>.'),
                    q('(√1764 + ∛2744) × 3 − 25 = ?',
                      ['143', '139', '147', '151', '135'],
                      0, '√1764 = 42, ∛2744 = 14 → (42 + 14) × 3 − 25 = 168 − 25 = <b>143</b>.'),
                    q('1260 ÷ 14 × 3 − ? = 12² + 6',
                      ['100', '110', '115', '120', '130'],
                      3, '1260 ÷ 14 × 3 = 270; 12² + 6 = 150 → ? = 270 − 150 = <b>120</b>.'),
                    q('3/5 of 2/7 of 5/12 of 2520 = ?',
                      ['160', '175', '180', '210', '240'],
                      2, '5/12 × 2520 = 1050; 2/7 × 1050 = 300; 3/5 × 300 = <b>180</b>.'),
                    q('?% of 480 + 25% of 360 = 186',
                      ['15', '18', '22', '25', '20'],
                      4, '25% of 360 = 90 → ?% of 480 = 96 → ? = 96 × 100 / 480 = <b>20</b>.'),
                ],
            },
            {
                'topic': 'Number Series',
                'directions': 'Directions (36–40): What value should come in place of the question mark (?) in the following number series?',
                'layout': 'inline',
                'questions': [
                    q('7, 15, 31, 63, ?, 255',
                      ['125', '127', '129', '131', '119'],
                      1, 'Each term = previous × 2 + 1 → 63 × 2 + 1 = <b>127</b>.'),
                    q('4, 6, 12, 30, 90, ?',
                      ['270', '300', '315', '360', '280'],
                      2, 'Multipliers are ×1.5, ×2, ×2.5, ×3, ×3.5 → 90 × 3.5 = <b>315</b>.'),
                    q('120, 99, 80, 63, 48, ?',
                      ['33', '35', '37', '36', '38'],
                      1, 'Differences are −21, −19, −17, −15, −13 → 48 − 13 = <b>35</b>.'),
                    q('2, 3, 11, 38, 102, ?',
                      ['215', '221', '227', '233', '240'],
                      2, 'Differences are 1³, 2³, 3³, 4³, 5³ → 102 + 125 = <b>227</b>.'),
                    q('5, 11, 24, 51, 106, ?',
                      ['211', '213', '215', '219', '217'],
                      4, 'Pattern: ×2 + 1, ×2 + 2, ×2 + 3, ×2 + 4, ×2 + 5 → 106 × 2 + 5 = <b>217</b>.'),
                ],
            },
            {
                'topic': 'Quadratic Equations',
                'directions': 'Directions (41–45): In each of the following questions, two equations (I) and (II) are given. Solve both equations and mark the correct relationship between x and y.',
                'layout': 'inline',
                'questions': [
                    q('I. x² − 11x + 30 = 0<br>II. y² − 7y + 12 = 0',
                      QUADRATIC_OPTIONS, 0, 'x = 5, 6; y = 3, 4. Every value of x is greater than every value of y → <b>x &gt; y</b>.'),
                    q('I. x² + 9x + 20 = 0<br>II. y² + 5y + 6 = 0',
                      QUADRATIC_OPTIONS, 1, 'x = −4, −5; y = −2, −3. Every x is smaller than every y → <b>x &lt; y</b>.'),
                    q('I. x² − 8x + 15 = 0<br>II. y² − 3y − 10 = 0',
                      QUADRATIC_OPTIONS, 4, 'x = 3, 5; y = 5, −2. x = 3 is less than y = 5 but greater than y = −2 → relationship cannot be established.'),
                    q('I. 2x² − 13x + 21 = 0<br>II. y² − 6y + 9 = 0',
                      QUADRATIC_OPTIONS, 2, 'x = 3.5, 3; y = 3 → <b>x ≥ y</b>.'),
                    q('I. x² + 2x − 8 = 0<br>II. y² − 4y + 4 = 0',
                      QUADRATIC_OPTIONS, 3, 'x = 2, −4; y = 2 → <b>x ≤ y</b>.'),
                ],
            },
            {
                'topic': 'Data Interpretation',
                'directions': 'Directions (46–50): Study the following table carefully and answer the questions given below.',
                'body': DI_TABLE,
                'layout': 'split',
                'questions': [
                    q('What is the total number of applications approved by all five banks together?',
                      ['3740', '3820', '3880', '3920', '3780'],
                      1, DI_WORKING + ' Total = 780 + 720 + 720 + 880 + 720 = <b>3820</b>.'),
                    q('What is the ratio of the number of applications rejected by Bank B to that rejected by Bank D?',
                      ['12 : 13', '13 : 11', '13 : 12', '11 : 12', '6 : 5'],
                      2, 'Rejected by B = 1500 − 720 = 780; by D = 1600 − 880 = 720 → 780 : 720 = <b>13 : 12</b>.'),
                    q('The number of home loans approved by Bank C is what percent more than that approved by Bank B?',
                      ['80%', '90%', '100%', '120%', '75%'],
                      2, DI_WORKING + ' (360 − 180) / 180 × 100 = <b>100%</b>.'),
                    q('What is the average number of home loans approved by Banks A, C and E?',
                      ['322', '328', '336', '332', '340'],
                      3, DI_WORKING + ' (312 + 360 + 324) / 3 = 996 / 3 = <b>332</b>.'),
                    q('Which bank approved the highest number of loans other than home loans?',
                      ['A', 'B', 'C', 'E', 'D'],
                      4, 'Non-home approvals: A 468, B 540, C 360, D 572, E 396 → <b>D</b>.'),
                ],
            },
            {
                'topic': 'Arithmetic',
                'questions': [
                    q('A\'s salary is 25% more than B\'s salary. By what percent is B\'s salary less than A\'s salary?',
                      ['25%', '20%', '22.5%', '18%', '15%'],
                      1, 'If B = 100, A = 125. B is less by 25/125 × 100 = <b>20%</b>.'),
                    q('A shopkeeper marks an article 40% above its cost price and allows a discount of 15% on the marked price. What is his profit percentage?',
                      ['25%', '21%', '17%', '19%', '23%'],
                      3, 'SP = 1.40 × 0.85 × CP = 1.19 CP → profit = <b>19%</b>.'),
                    q('What is the difference between the compound interest and the simple interest on ₹12,000 for 2 years at 10% per annum, interest compounded annually?',
                      ['₹100', '₹110', '₹120', '₹130', '₹144'],
                      2, 'Difference for 2 years = P(r/100)² = 12000 × 0.01 = <b>₹120</b>.'),
                    q('A can complete a work in 12 days and B can complete it in 18 days. They work together for 4 days, after which A leaves. In how many days will B finish the remaining work?',
                      ['6 days', '7 days', '8 days', '9 days', '10 days'],
                      2, 'Together per day = 1/12 + 1/18 = 5/36. In 4 days: 20/36 = 5/9. Remaining 4/9 × 18 = <b>8 days</b>.'),
                    q('A train 240 m long running at 54 km/h crosses a platform in 28 seconds. What is the length of the platform?',
                      ['160 m', '180 m', '200 m', '220 m', '150 m'],
                      1, '54 km/h = 15 m/s. Distance in 28 s = 420 m → platform = 420 − 240 = <b>180 m</b>.'),
                    q('The speed of a boat in still water is 15 km/h and the speed of the stream is 3 km/h. How long will the boat take to go 54 km upstream and return?',
                      ['7 hours', '7.5 hours', '8 hours', '6.5 hours', '9 hours'],
                      1, 'Upstream 12 km/h → 4.5 h; downstream 18 km/h → 3 h. Total = <b>7.5 hours</b>.'),
                    q('The ratio of the present ages of P and Q is 5 : 7. After 6 years the ratio will be 7 : 9. What is Q\'s present age?',
                      ['14 years', '18 years', '24 years', '21 years', '28 years'],
                      3, '(5k + 6)/(7k + 6) = 7/9 → 45k + 54 = 49k + 42 → k = 3 → Q = <b>21 years</b>.'),
                    q('A and B start a business with ₹30,000 and ₹45,000 respectively. After 4 months, A invests ₹15,000 more. If the profit at the end of the year is ₹51,000, what is B\'s share?',
                      ['₹24,000', '₹25,500', '₹27,000', '₹28,500', '₹30,000'],
                      2, 'A = 30000 × 4 + 45000 × 8 = 4,80,000; B = 45000 × 12 = 5,40,000 → 8 : 9. B = 51000 × 9/17 = <b>₹27,000</b>.'),
                    q('A 60-litre mixture contains milk and water in the ratio 7 : 3. How much water must be added to make the ratio 3 : 2?',
                      ['8 litres', '10 litres', '12 litres', '15 litres', '6 litres'],
                      1, 'Milk = 42 L, water = 18 L. 42/(18 + w) = 3/2 → w = <b>10 litres</b>.'),
                    q('The average age of 25 students is 48 months. When the teacher\'s age is included, the average increases by 1 month. What is the teacher\'s age in months?',
                      ['70', '72', '74', '76', '78'],
                      2, '26 × 49 − 25 × 48 = 1274 − 1200 = <b>74 months</b>.'),
                    q('A bag contains 5 red, 4 blue and 3 green balls. Two balls are drawn at random. What is the probability that both are of the same colour?',
                      ['19/66', '17/66', '5/22', '1/3', '7/22'],
                      0, '(⁵C₂ + ⁴C₂ + ³C₂) / ¹²C₂ = (10 + 6 + 3) / 66 = <b>19/66</b>.'),
                    q('The length and breadth of a rectangle are in the ratio 4 : 3 and its perimeter is 84 m. What is the length of its diagonal?',
                      ['25 m', '28 m', '32 m', '35 m', '30 m'],
                      4, '2(4k + 3k) = 84 → k = 6 → 24 m × 18 m → diagonal = √(576 + 324) = <b>30 m</b>.'),
                    q('Pipes A and B can fill a tank in 20 minutes and 30 minutes respectively, while pipe C can empty it in 15 minutes. If all three are opened together, in how much time will the empty tank be filled?',
                      ['45 minutes', '50 minutes', '60 minutes', '75 minutes', '90 minutes'],
                      2, 'Net per minute = 1/20 + 1/30 − 1/15 = 1/60 → <b>60 minutes</b>.'),
                    q('A car covers the first half of a journey at 40 km/h and the second half at 60 km/h. What is its average speed for the whole journey?',
                      ['50 km/h', '48 km/h', '45 km/h', '52 km/h', '46 km/h'],
                      1, 'For equal distances, average = 2 × 40 × 60 / (40 + 60) = <b>48 km/h</b>.'),
                    q('In an examination, 35% of the candidates failed in English, 25% failed in Mathematics and 10% failed in both. If 1500 candidates passed in both subjects, how many candidates appeared?',
                      ['2500', '2800', '3200', '3000', '3500'],
                      3, 'Failed in at least one = 35 + 25 − 10 = 50%, so 50% passed both = 1500 → total = <b>3000</b>.'),
                ],
            },
        ],
    },
    {
        'name': 'Reasoning Ability',
        'minutes': 20,
        'groups': [
            {
                'topic': 'Circular Seating',
                'directions': 'Directions (66–70): Study the following information carefully and answer the questions given below.',
                'body': CIRCULAR,
                'layout': 'split',
                'questions': [
                    q('Who sits second to the right of T?', ['W', 'Q', 'R', 'U', 'V'], 2, CIRCULAR_SOLUTION + ' Second to the right of T is R.'),
                    q('How many persons sit between U and Q when counted from the left of U?', ['One', 'Two', 'Four', 'Three', 'Five'], 3, CIRCULAR_SOLUTION + ' Going left (clockwise) from U: R, W, T, then Q — three persons.'),
                    q('Which of the following pairs are immediate neighbours?', ['Q and W', 'V and S', 'T and R', 'U and W', 'P and R'], 1, CIRCULAR_SOLUTION + ' V and S sit next to each other.'),
                    q('Four of the following five are alike in a certain way based on their positions and so form a group. Which one does not belong to that group?', ['P – R', 'U – W', 'R – T', 'T – S', 'W – Q'], 3, CIRCULAR_SOLUTION + ' In each pair the second person sits second to the left of the first, except T – S (second to the left of T is V).'),
                    q('Who sits exactly opposite W?', ['P', 'U', 'V', 'Q', 'S'], 4, CIRCULAR_SOLUTION + ' S sits opposite W.'),
                ],
            },
            {
                'topic': 'Floor Puzzle',
                'directions': 'Directions (71–75): Study the following information carefully and answer the questions given below.',
                'body': FLOORS,
                'layout': 'split',
                'questions': [
                    q('Who lives on the 5th floor?', ['A', 'B', 'G', 'F', 'D'], 2, FLOORS_SOLUTION),
                    q('Which fruit does C like?', ['Cherry', 'Grapes', 'Orange', 'Banana', 'Kiwi'], 1, FLOORS_SOLUTION),
                    q('How many persons live between A and F?', ['None', 'One', 'Three', 'Two', 'Four'], 3, FLOORS_SOLUTION + ' G (5) and B (4) live between A (6) and F (3).'),
                    q('Who lives immediately below the one who likes Orange?', ['C', 'G', 'E', 'A', 'F'], 4, FLOORS_SOLUTION + ' B likes Orange (floor 4); F lives on floor 3.'),
                    q('Which of the following statements is true?', ['A likes Kiwi', 'C lives on floor 3', 'G lives immediately above A', 'E likes Banana', 'F likes Orange'], 3, FLOORS_SOLUTION),
                ],
            },
            {
                'topic': 'Syllogism',
                'directions': 'Directions (76–78): In each question below are given some statements followed by two conclusions. Take the statements to be true even if they seem to be at variance with commonly known facts, and decide which of the conclusions logically follows.',
                'layout': 'inline',
                'questions': [
                    q('<b>Statements:</b> All pens are books. Some books are tables. No table is a chair.<br><b>Conclusions:</b><br>I. Some pens are tables.<br>II. Some books are not chairs.',
                      SYLLOGISM_OPTIONS, 1, 'I does not follow — the books that are tables need not be pens. II follows — the books that are tables can never be chairs.'),
                    q('<b>Statements:</b> Some cups are plates. All plates are spoons. No spoon is a knife.<br><b>Conclusions:</b><br>I. Some cups are spoons.<br>II. No plate is a knife.',
                      SYLLOGISM_OPTIONS, 4, 'Some cups are plates + all plates are spoons → some cups are spoons. All plates are spoons + no spoon is a knife → no plate is a knife. Both follow.'),
                    q('<b>Statements:</b> Only a few rivers are lakes. All lakes are ponds. No pond is a sea.<br><b>Conclusions:</b><br>I. Some rivers are not lakes.<br>II. All rivers being seas is a possibility.',
                      SYLLOGISM_OPTIONS, 0, '"Only a few rivers are lakes" means some rivers are not lakes — I follows. The rivers that are lakes are ponds and so can never be seas — II does not follow.'),
                ],
            },
            {
                'topic': 'Inequality',
                'directions': 'Directions (79–81): In each question, a relationship between different elements is shown in the statement(s). The statement(s) is followed by two conclusions. Mark the appropriate answer.',
                'layout': 'inline',
                'questions': [
                    q('<b>Statement:</b> P ≥ Q > R = S ≤ T<br><b>Conclusions:</b><br>I. P > S<br>II. T > R',
                      INEQUALITY_OPTIONS, 0, 'P ≥ Q > R = S gives P > S — I is true. T ≥ S = R gives only T ≥ R — II is not definitely true.'),
                    q('<b>Statement:</b> A > B ≥ C = D < E; F ≤ D<br><b>Conclusions:</b><br>I. A > F<br>II. E > F',
                      INEQUALITY_OPTIONS, 4, 'A > B ≥ C = D ≥ F → A > F. E > D ≥ F → E > F. Both are true.'),
                    q('<b>Statement:</b> G ≥ H = I ≤ J; K ≤ I<br><b>Conclusions:</b><br>I. G > K<br>II. G = K',
                      INEQUALITY_OPTIONS, 2, 'G ≥ H = I ≥ K gives G ≥ K. So either G > K or G = K — one of the two must be true.'),
                ],
            },
            {
                'topic': 'Coding-Decoding',
                'directions': 'Directions (82–84): In a certain code language:<br>"bank loan rate high" is written as "mo ki la pe",<br>"rate cut home loan" is written as "ki zu ra mo",<br>"high home price" is written as "pe ra tu", and<br>"cut price now" is written as "tu zu xi".',
                'layout': 'inline',
                'questions': [
                    q('What is the code for "bank"?', ['mo', 'pe', 'ki', 'la', 'ra'], 3, 'loan/rate = mo/ki (sentences 1 & 2), high = pe (1 & 3). The remaining code in sentence 1 is la = bank.'),
                    q('What is the code for "home"?', ['ra', 'zu', 'tu', 'pe', 'xi'], 0, '"home" is common to sentences 2 and 3; the common code is ra.'),
                    q('Which of the following is the code for "loan"?', ['ki', 'mo', 'Either mo or ki', 'zu', 'la'], 2, '"loan" and "rate" both appear only in sentences 1 and 2, sharing the codes mo and ki — it cannot be determined which is which.'),
                ],
            },
            {
                'topic': 'Blood Relation',
                'questions': [
                    q('Pointing to a man, Riya said, "He is the son of the only son of my grandfather." How is the man related to Riya?',
                      ['Cousin', 'Uncle', 'Brother', 'Nephew', 'Father'],
                      2, 'The only son of Riya\'s grandfather is her father; his son is her <b>brother</b>.'),
                ],
            },
            {
                'topic': 'Blood Relation',
                'directions': 'Directions (86–87): P is the mother of Q. Q is the sister of R. R is married to S. S is the daughter of T. T is the husband of U.',
                'layout': 'inline',
                'questions': [
                    q('How is U related to R?', ['Mother', 'Mother-in-law', 'Aunt', 'Sister-in-law', 'Grandmother'], 1, 'U is the wife of T and the mother of S. R is married to S, so U is R\'s <b>mother-in-law</b>.'),
                    q('How is Q related to S?', ['Sister', 'Cousin', 'Mother-in-law', 'Daughter', 'Sister-in-law'], 4, 'Q is the sister of R, and R is married to S, so Q is S\'s <b>sister-in-law</b>.'),
                ],
            },
            {
                'topic': 'Direction Sense',
                'questions': [
                    q('Aman walks 10 m towards the north, turns right and walks 6 m, turns right again and walks 4 m, then turns left and walks 2 m. How far and in which direction is he from his starting point?',
                      ['10 m, North-East', '8 m, East', '12 m, North-East', '10 m, North-West', '6 m, North'],
                      0, 'Final position is 8 m east and 6 m north of the start → √(8² + 6²) = <b>10 m, North-East</b>.'),
                ],
            },
            {
                'topic': 'Direction Sense',
                'directions': 'Directions (89–90): Point A is 8 m west of point B. Point C is 6 m north of point B. Point D is 5 m east of point C. Point E is 6 m south of point D.',
                'layout': 'inline',
                'questions': [
                    q('What is the distance between points A and E?', ['11 m', '12 m', '13 m', '14 m', '15 m'], 2, 'Taking B as origin: A(−8, 0), E(5, 0). Distance = <b>13 m</b>.'),
                    q('In which direction is point D with respect to point A?', ['North', 'North-East', 'East', 'South-East', 'North-West'], 1, 'D(5, 6) is to the east and north of A(−8, 0) → <b>North-East</b>.'),
                ],
            },
            {
                'topic': 'Linear Seating',
                'directions': 'Directions (91–95): Study the following information carefully and answer the questions given below.',
                'body': LINEAR,
                'layout': 'split',
                'questions': [
                    q('How many persons sit to the right of Y?', ['One', 'Two', 'Three', 'Four', 'None'], 1, LINEAR_SOLUTION + ' K and M sit to the right of Y.'),
                    q('Who sits exactly in the middle of J and Y?', ['O', 'N', 'K', 'X', 'M'], 0, LINEAR_SOLUTION),
                    q('Who sits to the immediate right of X?', ['L', 'J', 'O', 'N', 'Y'], 3, LINEAR_SOLUTION),
                    q('Which of the following pairs sits at the extreme ends of the row?', ['L and K', 'X and M', 'L and M', 'J and M', 'L and Y'], 2, LINEAR_SOLUTION),
                    q('How many persons sit between L and O?', ['Two', 'Four', 'One', 'Three', 'Five'], 3, LINEAR_SOLUTION + ' X, N and J sit between L and O.'),
                ],
            },
            {
                'topic': 'Number Arrangement',
                'directions': 'Directions (96–98): The following questions are based on the five three-digit numbers given below.',
                'body': NUMBERS,
                'layout': 'inline',
                'questions': [
                    q('If the digits within each number are arranged in ascending order, which of the following will be the largest number?',
                      ['734', '921', '586', '469', '358'],
                      2, 'New numbers: 347, 568, 129, 469, 358 → the largest, 568, comes from <b>586</b>.'),
                    q('What is the sum of the first and the third digits of the second-highest number?',
                      ['10', '11', '12', '13', '9'],
                      1, 'In descending order: 921, 734, 586, 469, 358. Second-highest is 734 → 7 + 4 = <b>11</b>.'),
                    q('If the positions of the first and the second digits of each number are interchanged, which of the following will be the smallest number?',
                      ['734', '586', '469', '921', '358'],
                      3, 'New numbers: 374, 856, 291, 649, 538 → the smallest, 291, comes from <b>921</b>.'),
                ],
            },
            {
                'topic': 'Order & Ranking',
                'questions': [
                    q('In a row of 40 students, Rohan is 14th from the left end and Mira is 17th from the right end. How many students sit between Rohan and Mira?',
                      ['8', '10', '11', '9', '7'],
                      3, 'Mira is 40 − 17 + 1 = 24th from the left. Students between = 24 − 14 − 1 = <b>9</b>.'),
                ],
            },
            {
                'topic': 'Alphabet Test',
                'questions': [
                    q('How many pairs of letters are there in the word <b>DEPOSIT</b> which have as many letters between them in the word as in the English alphabet (in both forward and backward directions)?',
                      ['Two', 'Three', 'Four', 'Five', 'More than five'],
                      3, 'The pairs are DE, DI, EI, PO and PT — <b>five</b>.'),
                ],
            },
        ],
    },
]

PLAN = {
    'name': 'IBPS PO Pro Pack',
    'price_inr': 199,
    'mrp_inr': 499,
    'features': '\n'.join([
        '12 full-length IBPS PO Prelims mocks',
        'Exact TCS iON exam-day interface',
        'Section-wise score, accuracy and time analysis',
        'Detailed solutions for every question',
        'Valid till your exam date',
    ]),
}

PRO_MOCKS = 12
