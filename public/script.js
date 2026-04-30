if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
}

const CATEGORIES = [
    {
        title: 'II. Pagtrato at Pangangalaga ng mga Nars (Treatment and Care of Nurses)',
        key: 'II. Pagtrato at Pangangalaga ng mga Nars',
        questions: [
            "Maayos at may paggalang ang pakikitungo sa akin ng mga nars.\n(The nurses treated me properly and with respect.)",
            "Ipinakita ng mga nars ang malasakit sa aking kalagayan.\n(The nurses showed concern for my condition.)",
            "Agad na tinugunan ng mga nars ang aking pangangailangan.\n(The nurses immediately attended to my needs.)",
            "Pinadama sa akin ng mga nars ang pagiging komportable habang ako ay ginagamot at inaalagaan.\n(The nurses made me feel comfortable during my treatment and care.)"
        ]
    },
    {
        title: 'III. Pagbibigay ng Impormasyon (Provision of Information)',
        key: 'III. Pagbibigay ng Impormasyon',
        questions: [
            "Ipinaliwanag ng mga nars ang mga gagawing pamamaraan bago ito isagawa.\n(The nurses explained the procedures before they were performed.)",
            "Maliwanag nilang ipinaalam ang tungkol sa aking gamot.\n(They clearly informed me about my medication.)",
            "Nasagot nang maayos ng mga nars ang aking mga tanong.\n(The nurses answered my questions properly.)",
            "Naipaliwanag nila ang mahahalagang impormasyon tungkol sa aking kalagayan.\n(They explained important information about my condition.)"
        ]
    },
    {
        title: 'IV. Kakayahan ng mga Nars (Competence of Nurses)',
        key: 'IV. Kakayahan ng mga Nars',
        questions: [
            "Maayos at maingat gumawa ng tungkulin ang mga nars.\n(The nurses performed their duties properly and carefully.)",
            "Nagpakita sila ng kaalaman sa kanilang trabaho.\n(They showed knowledge in their work.)",
            "Naging maingat sila sa pagbibigay ng pangangalaga sa akin.\n(They were careful in giving care to me.)",
            "Naging handa at mabilis sila sa oras ng pangangailangan.\n(They were prepared and quick during times of need.)"
        ]
    },
    {
        title: 'V. Pangkalahatang Kasiyahan (Overall Satisfaction)',
        key: 'V. Pangkalahatang Kasiyahan',
        questions: [
            "Ako ay nasiyahan sa serbisyong ibinigay ng mga nars.\n(I am satisfied with the service provided by the nurses.)",
            "Nakatulong ang mga nars sa aking paggaling.\n(The nurses helped in my recovery.)",
            "Maganda ang naging karanasan ko sa pangangalaga ng mga nars.\n(I had a good experience with the nursing care.)",
            "Irerekomenda ko ang ospital na ito dahil sa mahusay na serbisyo ng mga nars.\n(I would recommend this hospital because of the excellent nursing service.)"
        ]
    }
];

const RATING_LABELS = {
    1: 'Lubos na Hindi Sumasang-ayon',
    2: 'Hindi Sumasang-ayon',
    3: 'Neutral',
    4: 'Sumasang-ayon',
    5: 'Lubos na Sumasang-ayon'
};

const TOTAL_STEPS = 5;
let currentStep = 1;
let qIndex = 0;

// Build survey steps dynamically
function buildSurveySteps() {
    const container = document.getElementById('surveySteps');
    let stepNum = 2;
    qIndex = 0;

    CATEGORIES.forEach((cat, catIdx) => {
        const isLast = catIdx === CATEGORIES.length - 1;
        const questionsHTML = cat.questions.map(q => {
            const fn = `q_${qIndex}`;
            const ratingsHTML = [1,2,3,4,5].map(r => `
                <div class="rating-option">
                    <input type="radio" id="${fn}_${r}" name="${fn}" value="${r}" data-question="${qIndex}">
                    <label for="${fn}_${r}" class="rating-label">
                        <span class="rating-number">${r}</span>
                        <span class="rating-text">${RATING_LABELS[r]}</span>
                    </label>
                </div>`).join('');
            const html = `
                <div class="question-card" data-question="${qIndex}">
                    <label class="question-label">${q.replace(/\n/g, '<br>')}</label>
                    <div class="rating-group">${ratingsHTML}</div>
                    <span class="error-message">Kailangan ang sagot sa tanong na ito</span>
                </div>`;
            qIndex++;
            return html;
        }).join('');

        container.innerHTML += `
            <div class="form-step" data-step="${stepNum}">
                <div class="form-section">
                    <div class="section-title">${cat.title}</div>
                    <p class="helper-text">Pumili ng sagot mula 1 hanggang 5 para sa bawat tanong.</p>
                    ${questionsHTML}
                </div>
                <div class="step-navigation">
                    <button type="button" class="btn-prev">Balik</button>
                    ${isLast
                        ? '<button type="submit" class="btn-submit" id="submitBtn">Isumite</button>'
                        : '<button type="button" class="btn-next">Susunod</button>'
                    }
                </div>
            </div>`;
        stepNum++;
    });
}

document.addEventListener('DOMContentLoaded', function () {
    buildSurveySteps();

    const form = document.getElementById('surveyForm');
    const successMessage = document.getElementById('successMessage');
    const progressBar = document.getElementById('progressBar');
    const stepIndicator = document.getElementById('stepIndicator');

    showStep(currentStep);
    updateProgress();

    // Radio change — clear error
    document.addEventListener('change', function (e) {
        if (e.target.type === 'radio') {
            e.target.closest('.question-card')?.classList.remove('error');
        }
    });

    // Input/select change — clear error
    document.addEventListener('input', function (e) {
        e.target.closest('.form-group')?.classList.remove('error');
    });

    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('btn-next')) nextStep();
        if (e.target.classList.contains('btn-prev')) prevStep();
    });

    form.addEventListener('submit', handleSubmit);

    function showStep(step) {
        document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
        document.querySelector(`.form-step[data-step="${step}"]`)?.classList.add('active');
        stepIndicator.textContent = `Hakbang ${step} ng ${TOTAL_STEPS}`;
        const prev = document.querySelector('.form-step.active .btn-prev');
        if (prev) prev.disabled = step === 1;
    }

    function updateProgress() {
        progressBar.style.width = (currentStep / TOTAL_STEPS * 100) + '%';
    }

    function nextStep() {
        if (validate()) {
            currentStep++;
            showStep(currentStep);
            updateProgress();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    function prevStep() {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
            updateProgress();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    function validate() {
        let valid = true;
        let first = null;
        const active = document.querySelector('.form-step.active');

        if (currentStep === 1) {
            active.querySelectorAll('input, select').forEach(f => {
                if (!f.value.trim()) {
                    f.closest('.form-group').classList.add('error');
                    valid = false;
                    if (!first) first = f;
                } else {
                    f.closest('.form-group').classList.remove('error');
                }
            });
        } else {
            active.querySelectorAll('.question-card').forEach(card => {
                const answered = Array.from(card.querySelectorAll('input[type="radio"]')).some(r => r.checked);
                if (!answered) {
                    card.classList.add('error');
                    valid = false;
                    if (!first) first = card;
                } else {
                    card.classList.remove('error');
                }
            });
        }

        if (!valid && first) first.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return valid;
    }

    async function handleSubmit(e) {
        e.preventDefault();

        // Validate all steps
        for (let s = 1; s <= TOTAL_STEPS; s++) {
            currentStep = s;
            showStep(s);
            if (!validate()) {
                alert('Pakisagutan ang lahat ng tanong at impormasyon.');
                return;
            }
        }

        if (!confirm('Sigurado ka bang isusumite ang survey na ito?')) return;

        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Ipinapadala...';

        // Collect answers
        const answers = {};
        document.querySelectorAll('input[type="radio"]:checked').forEach(r => {
            answers[r.name] = parseInt(r.value);
        });

        const payload = {
            name: document.getElementById('name').value.trim(),
            age: parseInt(document.getElementById('age').value),
            sex: document.getElementById('sex').value,
            civil_status: document.getElementById('civil_status').value,
            duration_of_hospitalization: document.getElementById('duration_of_hospitalization').value.trim(),
            ward: document.getElementById('ward').value.trim(),
            answers
        };

        try {
            const res = await fetch('/api/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (data.success) {
                successMessage.classList.add('show');
                window.scrollTo({ top: 0, behavior: 'smooth' });
                form.querySelectorAll('input, select, button').forEach(el => el.disabled = true);
                submitBtn.textContent = '✓ Naisumite na';
            } else {
                alert('May error: ' + (data.message || 'Unknown error'));
                submitBtn.disabled = false;
                submitBtn.textContent = 'Isumite';
            }
        } catch {
            alert('May problema sa pagpadala. Subukan ulit.');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Isumite';
        }
    }
});
