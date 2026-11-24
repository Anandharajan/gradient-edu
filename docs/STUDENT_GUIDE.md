# Student guide: from video to marks

1. **Learn**: open the app, watch the lesson video, read the notes, and score at least 70% on the quiz (⚡ XP, 🔥 streaks!).
2. **Play**: try the unit's sandbox to see the algorithm in action.
3. **Start lab**: on the 🏰 lab page click **Start lab**. GitHub's *Create repository* page opens with everything
   filled in (template, name `cs3491-lab-NN-…`, **Private**) — click **Create repository**.
   Then in your new repo: **Settings → Collaborators → Add people → `Anandharajan`** (once per lab, so it can be graded).
4. **Code**:
   ```bash
   git clone <your repo url> && cd <repo>
   pip install -r requirements.txt
   # edit src/labNN.py (do not rename functions)
   gradient-edu check            # public tests + lint + report check
   ```
   No laptop? Click **Code → Codespaces** in your repo for VS Code in the browser.
5. **Report**: fill the four sections of `REPORT.md` in your own words (20+ words each).
6. **Push**: `git add . && git commit -m "Lab NN" && git push`
7. **Marks**: within ~15 minutes `GRADE.md` in your repo shows every hidden test ✅/❌ and your marks. Fix, push again, and your best attempt counts.
8. **Viva**: your teacher adds 15 marks after asking you to explain your code.
9. **Track**: the app's **Progress** page shows your CO mastery and all 13 lab marks.

**Rules:** write your own code (similarity is checked); late pushes lose 2 marks per day; AI tools are allowed only if you can explain every line in the viva.
