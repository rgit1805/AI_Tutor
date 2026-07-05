document.addEventListener('DOMContentLoaded', () => {
    // Requires student from app.js
    if (!student) return;

    const topicInput = document.getElementById('topicInput');
    const timeframeInput = document.getElementById('timeframeInput');
    const generateBtn = document.getElementById('generatePlanBtn');
    const loading = document.getElementById('loadingIndicator');
    const planResult = document.getElementById('planResult');
    const planTitle = document.getElementById('planTitle');
    const planContent = document.getElementById('planContent');
    const historyContainer = document.getElementById('historyContainer');

    async function loadHistory() {
        try {
            const res = await fetch(`/study_api/history/${student.student_id}`);
            const plans = await res.json();
            
            if (plans.length === 0) {
                historyContainer.innerHTML = '<p style="opacity:0.7;">No past study plans found.</p>';
            } else {
                historyContainer.innerHTML = plans.reverse().map(p => `
                    <div class="history-item" onclick="viewPlan(${p.id})">
                        <strong style="display:block; margin-bottom: 0.3rem;">${p.topic}</strong>
                        <span style="font-size:0.85rem; opacity:0.8;">${p.timeframe}</span>
                    </div>
                `).join('');
                
                // Store globally to view easily
                window.pastPlans = plans;
            }
        } catch (e) {
            console.error("Error loading history:", e);
        }
    }

    window.viewPlan = function(id) {
        const plan = window.pastPlans.find(p => p.id === id);
        if (plan) {
            planTitle.innerText = `${plan.topic} (${plan.timeframe})`;
            planContent.innerHTML = marked.parse(plan.plan_content);
            planResult.style.display = 'block';
            window.scrollTo({ top: planResult.offsetTop, behavior: 'smooth' });
        }
    }

    if (generateBtn) {
        generateBtn.addEventListener('click', async () => {
            const topic = topicInput.value.trim();
            const timeframe = timeframeInput.value.trim();

            if (!topic || !timeframe) {
                alert("Please enter both a topic and timeframe.");
                return;
            }

            generateBtn.disabled = true;
            loading.style.display = 'block';
            planResult.style.display = 'none';

            try {
                const res = await fetch('/study_api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        student_id: student.student_id,
                        topic: topic,
                        timeframe: timeframe
                    })
                });
                
                const data = await res.json();
                if (res.ok) {
                    planTitle.innerText = `${topic} (${timeframe})`;
                    planContent.innerHTML = marked.parse(data.plan_content);
                    planResult.style.display = 'block';
                    
                    // Clear inputs and reload history
                    topicInput.value = '';
                    timeframeInput.value = '';
                    loadHistory();
                } else {
                    alert(data.detail || "Failed to generate plan.");
                }
            } catch (e) {
                console.error("Generate plan error:", e);
                alert("Network error while generating plan.");
            } finally {
                generateBtn.disabled = false;
                loading.style.display = 'none';
            }
        });
    }

    // Initial load
    loadHistory();
});
