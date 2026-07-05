window.onerror = function (msg, url, lineNo, columnNo, error) {
    alert("JS Error: " + msg + "\nAt: " + lineNo + ":" + columnNo);
    return false;
};

// --- Global State ---
let student = null;
let currentQuestions = [];
let currentIdx = 0;
let score = 0;
let quizSubject = "";

// --- Global Functions ---

async function loadProgress() {
    if (!student) return;
    const res = await fetch(`/progress/${student.student_id}`);
    const data = await res.json();

    document.getElementById('totalPoints').innerText = data.total_points;
    document.getElementById('avgScore').innerText = data.average_score + '%';
    document.getElementById('attemptsCount').innerText = data.attempts_count;
    document.getElementById('studentName').innerText = `${student.name}'s Progress`;

    const analyticRes = await fetch(`/analytics/${student.student_id}`);
    const analytics = await analyticRes.json();

    document.getElementById('bestSubject').innerText = analytics.best_subject;
    document.getElementById('weakSubject').innerText = "Calculating...";

    const container = document.getElementById('achievementsContainer');
    if (container && data.achievements) {
        if (data.achievements.length === 0) {
            container.innerHTML = '<p style="opacity: 0.6; font-style: italic;">No achievements earned yet. Keep taking quizzes to unlock them!</p>';
        } else {
            container.innerHTML = data.achievements.map(a => `
                <div class="glass-card" style="padding: 1rem; text-align: center; width: 150px;">
                    <div style="font-size: 2rem;">${a.icon}</div>
                    <div style="font-weight: bold;">${a.title}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">${a.description}</div>
                </div>
            `).join('');
        }
    }
}

async function initQuiz(subject, difficulty, useAI = false, count = 5) {
    try {
        quizSubject = subject;
        const titleEl = document.getElementById('quizTitle');
        if (titleEl) titleEl.innerText = `${subject} ${useAI ? '(AI Powered ✨)' : 'Challenge'} (${difficulty})`;

        console.log(`Fetching: /quiz/questions?subject=${subject}&difficulty=${difficulty}&ai=${useAI}&count=${count}`);
        const res = await fetch(`/quiz/questions?subject=${subject}&difficulty=${difficulty}&ai=${useAI}&count=${count}`);

        if (!res.ok) {
            const errText = await res.text();
            throw new Error(`Server returned ${res.status}: ${errText}`);
        }

        currentQuestions = await res.json();
        console.log("Questions loaded:", currentQuestions);

        if (currentQuestions.length === 0) {
            alert("No questions found for this subject/difficulty. Please try another.");
            window.location.href = '/';
            return;
        }
        currentIdx = 0;
        score = 0;
        showQuestion();
    } catch (err) {
        console.error("initQuiz Error:", err);
        alert("Error loading quiz: " + err.message);
    }
}

function showQuestion() {
    try {
        const q = currentQuestions[currentIdx];
        if (!q) throw new Error("Question undefined at index " + currentIdx);

        document.getElementById('questionText').innerText = q.text;
        const opts = document.getElementById('optionsContainer');
        opts.innerHTML = '';

        let options = Array.isArray(q.options) ? q.options : JSON.parse(q.options);

        options.forEach((opt, idx) => {
            const btn = document.createElement('button');
            btn.innerText = opt;
            btn.className = "option-btn";
            btn.onclick = () => selectOption(idx);
            opts.appendChild(btn);
        });
    } catch (err) {
        console.error("showQuestion Error:", err);
        alert("Error displaying question: " + err.message);
    }
}

function selectOption(idx) {
    const btns = document.querySelectorAll('.option-btn');
    const correctIdx = currentQuestions[currentIdx].correct;

    btns.forEach((btn, i) => {
        btn.disabled = true;
        if (i === correctIdx) btn.style.background = "#00f260";
        else if (i === idx) btn.style.background = "#ff4b2b";
    });

    if (idx === correctIdx) score++;

    setTimeout(() => {
        currentIdx++;
        if (currentIdx < currentQuestions.length) {
            showQuestion();
        } else {
            submitQuiz();
        }
    }, 1000);
}

async function submitQuiz() {
    if (!student) return;
    const finalPercent = (score / currentQuestions.length) * 100;
    const res = await fetch('/quiz/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            student_id: student.student_id,
            subject: quizSubject,
            score: finalPercent,
            time_taken: 60,
            difficulty: localStorage.getItem('nextDifficulty') || "Easy"
        })
    });
    const data = await res.json();

    localStorage.setItem('nextDifficulty', data.next_difficulty);

    document.getElementById('questionContainer').style.display = 'none';
    document.getElementById('resultContainer').style.display = 'block';
    document.getElementById('finalScore').innerText = Math.round(finalPercent);
    document.getElementById('performanceLevel').innerText = data.performance_level;
    document.getElementById('recommendationText').innerText = data.recommendation;
    document.getElementById('pointsEarned').innerText = data.points_earned;

    if (data.achievements.length > 0) {
        alert(`New Achievement Unlocked: ${data.achievements[0].title}!`);
    }
}

function renderMarkdown(text) {
    // Escape HTML first to prevent XSS
    let html = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    // Bold: **text** or __text__
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.+?)__/g, '<strong>$1</strong>');
    // Italic: *text* or _text_
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    html = html.replace(/_(.+?)_/g, '<em>$1</em>');
    // Inline code: `code`
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Newlines to <br>
    html = html.replace(/\n/g, '<br>');
    return html;
}

function addMessage(text, className) {
    const chatBox = document.getElementById('chatBox');
    if (!chatBox) return;
    const div = document.createElement('div');
    div.className = `message ${className}`;
    div.innerHTML = renderMarkdown(text);
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function typeWriter(text, className) {
    const chatBox = document.getElementById('chatBox');
    if (!chatBox) return;
    const div = document.createElement('div');
    div.className = `message ${className}`;
    chatBox.appendChild(div);

    let i = 0;
    const interval = setInterval(() => {
        // Render the accumulated text as markdown on each tick
        div.innerHTML = renderMarkdown(text.substring(0, i + 1));
        i++;
        chatBox.scrollTop = chatBox.scrollHeight;
        if (i >= text.length) clearInterval(interval);
    }, 20);
}

// --- Main execution ---

document.addEventListener('DOMContentLoaded', () => {
    try {
        const stored = localStorage.getItem('student');
        if (stored && stored !== "undefined") {
            student = JSON.parse(stored);
        }
    } catch (e) {
        console.error("Student parse error:", e);
    }

    const path = window.location.pathname;
    const normalizedPath = path.endsWith('/') && path.length > 1 ? path.slice(0, -1) : path;
    console.log("Current Path:", normalizedPath);

    if (!student && normalizedPath !== '/login' && normalizedPath !== '/register') {
        window.location.href = '/login';
        return;
    }

    if (student) {
        console.log("Student found:", student);

        if (document.getElementById('welcomeMsg')) {
            document.getElementById('welcomeMsg').innerText = `Welcome Back, ${student.name}!`;
        }

        if (normalizedPath === '/progress') {
            loadProgress();
        }

        if (normalizedPath === '/quiz') {
            const params = new URLSearchParams(window.location.search);
            const subject = params.get('subject') || "Mathematics";
            const useAI = params.get('ai') === 'true';
            const count = params.get('count') || "5";
            const difficulty = localStorage.getItem('nextDifficulty') || "Easy";
            console.log("Starting quiz:", subject, difficulty, "AI:", useAI, "Count:", count);
            initQuiz(subject, difficulty, useAI, count).catch(err => {
                console.error("Quiz init failed:", err);
                alert("Quiz failed to load check console: " + err.message);
            });
        }
    }

    // --- Authentication ---
    const regBtn = document.getElementById('regBtn');
    if (regBtn) {
        regBtn.addEventListener('click', async () => {
            const name = document.getElementById('regName').value;
            const username = document.getElementById('regUsername').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;

            const res = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, username, email, password })
            });
            const data = await res.json();
            if (res.ok) {
                alert('Success! Please login.');
                window.location.href = '/login';
            } else {
                alert(data.detail || 'Error');
            }
        });
    }

    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', async () => {
            const username_or_email = document.getElementById('loginId').value;
            const password = document.getElementById('loginPassword').value;

            const res = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username_or_email, password })
            });
            const data = await res.json();
            if (res.ok) {
                localStorage.setItem('student', JSON.stringify(data));
                window.location.href = '/';
            } else {
                alert(data.detail || 'Error');
            }
        });
    }

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('student');
            window.location.href = '/login';
        });
    }

    // --- Chat Logic ---
    const sendBtn = document.getElementById('sendBtn');
    const chatInput = document.getElementById('chatInput');
    if (sendBtn) {
        const sendMessage = async () => {
            const msg = chatInput.value.trim();
            if (!msg) return;

            addMessage(msg, 'user-message');
            chatInput.value = '';

            const res = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg })
            });
            const data = await res.json();
            typeWriter(data.reply, 'ai-message');
        };

        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    const startQuizBtn = document.getElementById('startQuizBtn');
    if (startQuizBtn) {
        startQuizBtn.addEventListener('click', () => {
            const sub = document.getElementById('subjectSelect').value;
            const ai = document.getElementById('aiToggle').checked;
            const count = document.getElementById('questionCount').value;
            window.location.href = `/quiz?subject=${sub}&ai=${ai}&count=${count}`;
        });
    }
});
