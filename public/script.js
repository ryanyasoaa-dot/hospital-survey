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
    },
    {
        title: 'VI. Clarity of Statements (Linaw ng mga Pahayag)',
        key: 'VI. Clarity of Statements',
        questions: [
            "The questions in the Digital Nursing Care Satisfaction Survey Form that I answered are clear and easy to understand.\n(Malinaw at madaling maunawaan ang mga tanong sa Digital Nursing Care Satisfaction Survey Form na aking sinagutan.)",
            "The statements used in the survey form are not confusing.\n(Hindi nakakalito ang mga pahayag na ginamit sa survey form.)",
            "The instructions are clear and easy to follow while answering the form.\n(Ang mga instruksyon ay malinaw at madaling sundin habang sinasagutan ang form.)",
            "Each question is well-constructed for accurate responses.\n(Ang bawat tanong ay maayos ang pagkakabuo para sa tamang pagsagot.)",
            "I easily understand the purpose of each question in the survey form.\n(Natintindihan ko agad ang layunin ng bawat tanong sa survey form.)"
        ]
    },
    {
        title: 'VII. Ease of Use (Kadalian ng Paggamit)',
        key: 'VII. Ease of Use',
        questions: [
            "The Digital Nursing Care Satisfaction Survey Form is easy to use.\n(Madaling gamitin ang Digital Nursing Care Satisfaction Survey Form.)",
            "I was able to easily navigate from one question to the next.\n(Madali akong nakapag-navigate mula sa isang tanong patungo sa susunod.)",
            "The process of answering the digital survey form is convenient.\n(Maginhawa ang proseso ng pagsagot sa digital survey form.)"
        ]
    },
    {
        title: 'VIII. Completeness of Responses (Kabuuan ng mga Sagot)',
        key: 'VIII. Completeness of Responses',
        questions: [
            "I was able to provide complete answers to each question.\n(Nagawa kong makapagbigay ng kumpletong sagot sa bawat tanong.)",
            "The choices provided are sufficient for me to express my responses properly.\n(Sapat ang mga pagpipilian upang maipahayag ko nang maayos ang aking sagot.)",
            "The survey form helped me express my overall experience.\n(Ang survey form ay nakatulong upang maipahayag ko ang aking kabuuang karanasan.)"
        ]
    },
    {
        title: 'IX. Efficiency (Kahusayan ng Pagsagot)',
        key: 'IX. Efficiency',
        questions: [
            "I was able to save time in answering the digital survey form.\n(Nakapagtipid ako ng oras sa pagsagot sa digital survey form.)",
            "It is faster to answer compared to traditional paper-based surveys.\n(Mas mabilis itong sagutan kumpara sa tradisyunal na papel na survey.)",
            "The process of answering the form is smooth and continuous.\n(Maayos at tuloy-tuloy ang proseso ng pagsagot sa form.)",
            "The digital survey form helped me provide feedback quickly.\n(Nakatulong ang digital survey form sa mabilis na pagbibigay ko ng feedback.)",
            "The digital survey form is effective in collecting my responses.\n(Epektibo ang digital survey form sa pangangalap ng aking mga sagot.)"
        ]
    },
    {
        title: 'X. User Satisfaction (Kasiyahan sa Paggamit)',
        key: 'X. User Satisfaction',
        questions: [
            "I am satisfied with my experience using the Digital Nursing Care Satisfaction Survey Form.\n(Nasiyahan ako sa aking karanasan sa paggamit ng Digital Nursing Care Satisfaction Survey Form.)",
            "I feel comfortable using the digital survey form.\n(Komportable akong gumamit ng digital survey form.)",
            "I would use this type of survey form again if given the chance.\n(Gagamitin ko muli ang ganitong uri ng survey form kung muling ipagagamit.)",
            "I would recommend the use of digital survey forms to other patients or respondents.\n(Irerekomenda ko ang paggamit ng digital survey forms sa ibang pasyente o respondents.)"
        ]
    },
    {
        title: 'XI. Accuracy (Katumpakan ng Nakuhang Impormasyon)',
        key: 'XI. Accuracy',
        questions: [
            "I did not notice any incorrect recording of my responses.\n(Wala akong napansing maling pag-record ng aking responses.)",
            "My answers were saved accurately and consistently.\n(Tama at consistent ang pag-save ng aking mga sagot.)"
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

const TOTAL_STEPS = CATEGORIES.length + 1;
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
