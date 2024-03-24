# DzTweets_pipeline
Data pipeline for DzTweets

The first normalization step is to replace:
• Mails with a token [MAIL]
• User tags with a token [USER]
• Hash tags with a token [HASH]
• Links with a token [LINK]

The second step is to normalize words (without tokenization). Let’s start with Latin based scripts (French, English,
Berber):
• Replace accentuated e’s and a’s with e and a respectively.
• The ending s must be deleted (plural; even if it is not a plural).
• French suffixes (ir, er, ement, ien, iens, euse, euses, eux) must be deleted.
• English suffixes (ly, al) must be deleted. If the word ends with ally, we delete just ly.
• Berber suffixes (ya, en) must be deleted. For example: iggarzen → iggarz, arnuyas → arnu
• English contractions must be transformed into their origin. Such as: it’s → it is, don’t → do not
• French contractions must be transformed into their origin. Such as: qu’ont → que ont, s’abstenir → se abstenir,
p’tit → petit.

DZ Arabizi has some Arabic rules as well as rules specific to Algerian population. The difference, it is written in
Latin script. These are the rules which must be implemented:
• Negation must be deleted (ma...ch). For example, mal9itch → l9it
• Suffix k, km variations must be deleted. ywaf9ek → ywaf9, ya3tik → ya3ti, 3ndk → 3nd, 3ndkm → 3nd
• Suffixes a, i, o, ou must be deleted when the radical is two letters or more. This must be after the last rule in
case of suffixes ak, ik, ok, ouk For example, yetfarjou → yetfarj, fhamto → fhamt, mousiba → mousib, wladi
→ wlad
• Suffixes h, ha must be deleted when the radical is two letters or more. For example, khatih → khati, katiha →
khati
Standard Arabic and Dz Arabic are written using specific Arabic script.

Don't forget to star the Repo ma friend !!
