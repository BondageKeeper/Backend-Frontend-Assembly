const PasswordInputChange = document.getElementById('password_input_change');
    NewPasswordEstimation = document.getElementById('new_password_estimation');
    let isNewPasswordValid = false;
    const NewPasswordBtn = document.getElementById('apply_new_password');

    PasswordInputChange.addEventListener('input', () => {
    newPasswordLength = PasswordInputChange.value.length;
    NewPasswordEstimation.classList.remove('text-red-400','text-orange-400','text-green-400');
    hasNewPasswordLetters = /[a-zA-Zа-яА-ЯёЁ]/.test(PasswordInputChange.value);
    hasNewPasswordDigits = /[0-9]/.test(PasswordInputChange.value);
    if (newPasswordLength === 0) {
        NewPasswordEstimation.classList.add('hidden');
        NewPasswordBtn.disabled = true;
    } else {
        NewPasswordEstimation.classList.remove('hidden');
        NewPasswordBtn.disabled = true;
        if (newPasswordLength < 4) {
            NewPasswordEstimation.innerText = 'Minimum 4 characters required';
            NewPasswordEstimation.classList.add('text-red-400');
            NewPasswordBtn.disabled = true;
        }
        else if (newPasswordLength >= 4 && newPasswordLength < 6) {
            NewPasswordEstimation.innerText = 'Weak Password';
            NewPasswordEstimation.classList.add('text-red-400');
            NewPasswordBtn.disabled = true;
        }
        else if (newPasswordLength >= 6 && newPasswordLength < 8) {
            if (hasNewPasswordLetters && hasNewPasswordDigits) {
                NewPasswordEstimation.innerText = 'Medium Password';
                NewPasswordEstimation.classList.add('text-orange-400');
                NewPasswordBtn.disabled = false;
                isNewPasswordValid = true;
            } else {
                NewPasswordEstimation.innerText = 'Weak Password';
                NewPasswordEstimation.classList.add('text-red-400');
                NewPasswordBtn.disabled = true;
            }
        }
        else if (newPasswordLength >= 8) {
            if (hasNewPasswordLetters && hasNewPasswordDigits) {
                NewPasswordEstimation.innerText = 'Excellent Password';
                NewPasswordEstimation.classList.add('text-green-400');
                isNewPasswordValid = true;
                NewPasswordBtn.disabled = false;
            } else {
                NewPasswordEstimation.innerText = 'Medium Password';
                NewPasswordEstimation.classList.add('text-orange-400');
                isNewPasswordValid = true;
                NewPasswordBtn.disabled = false;
            }
    }
    }
    });

    //Part of passport change
    let user_email = document.getElementById('email_input');
    NewPasswordBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (isNewPasswordValid) {
        fetch('https://cards-hub.website/password_page/update_password',{
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify({
            email : user_email.value.trim(),
            password : PasswordInputChange.value.trim()
    })
    })
    .then(res => res.json())
    .then(ChangedData => {console.log(ChangedData);
    alert("Password has been changed successfully!");
    })
    .catch(error => console.error('Description:', error));
    }
    });



    //Part of the dashboard:
    const TodoColumn = document.getElementById('todo_column');
    const ProgressColumn = document.getElementById('progress_column');
    const DoneColumn = document.getElementById('done_column');

    function renderAITasks(stepsArray) {
    // Clean old tasks
    TodoColumn.innerHTML = '';
    ProgressColumn.innerHTML = '';
    DoneColumn.innerHTML = '';

    //Create cards due to cycle
    stepsArray.forEach((stepText, index) => {
        const taskCard = document.createElement('div');

        //turn on a draggable effect(mode)
        taskCard.setAttribute('draggable', 'true');
        //here we give a bunch of class parameters
        taskCard.className = "my_task_card bg-white/10 border-3 border-[#7be0ad]/10 rounded-xl p-3 text-[#e7e5e5] text-sm font-medium shadow-sm hover:border-[#7be0ad]/50 transition-all cursor-grab active:cursor-grabbing flex items-center justify-between";
        taskCard.id = `task-${Date.now()}-${index}`;

        //add only text of the task including index(number of the card)
        taskCard.innerHTML = `
            <span>${stepText}</span>
            <span class="text-xs opacity-50 font-bold">#${index + 1}</span>
        `;

        //here we put listeners to listen to our mouse(at the moment when user just touched our card)
        taskCard.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', taskCard.id);
        });
        //at the moment when user just unpressed the card
        taskCard.addEventListener('dragend', () => {
            updateCounters();
        });

        //here we put ready card in the column(at this moment our card is being drown on the screen)
        TodoColumn.appendChild(taskCard);
    });

    // here we put a number in counter(how much cards we totally have)
    document.getElementById('todo_counter').innerText = stepsArray.length;
}

    DeleteFullBtn = document.getElementById('delete_cards_btn');
    DeleteFullBtn.addEventListener('click', () => {
        user_email = document.getElementById('email_input');
        fetch(`https://cards-hub.website/password_page/delete_cards/${user_email.value.trim()}`,{
            method: 'DELETE'
        })
        .then(res => res.json())
        .then(columnsData => {
        document.getElementById('todo_column').innerHTML = '';
        document.getElementById('progress_column').innerHTML = '';
        document.getElementById('done_column').innerHTML = '';
        updateCounters();
        });
    });


    function RenderSingleCard(cardText,cardId,index) {
        const taskCard = document.createElement('div');
            taskCard.setAttribute('draggable',true);
            taskCard.className = 'my_task_card bg-white/10 border-3 border-[#7be0ad]/10 rounded-xl p-3 text-[#e7e5e5] text-sm font-medium shadow-sm hover:border-[#7be0ad]/50 transition-all cursor-grab active:cursor-grabbing flex items-center justify-between';
            taskCard.id = `task-${Date.now()}-${cardId}-${index}`;
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = cardText;
            let cleanText = tempDiv.innerText.trim();
            cleanText = cleanText.replace(/#\d+\s*$/, '').trim();

            taskCard.innerHTML = `
                <span>${cleanText}</span>
                <span class="text-xs opacity-50 font-bold">#${index + 1}</span>
            `;
            taskCard.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', taskCard.id);
            });
            taskCard.addEventListener('dragend', () => {
            updateCounters();
            });
        document.getElementById(cardId).appendChild(taskCard);
    }


    let MainBackground = false;
    let isBoard = false;

    function LoadAndRenderCards() {
    user_email = document.getElementById('email_input');
    fetch(`https://cards-hub.website/password_page/upload_cards/${user_email.value.trim()}`)
    .then(res => res.json())
    .then(columnsData => {
    document.getElementById('todo_column').innerHTML = '';
    document.getElementById('progress_column').innerHTML = '';
    document.getElementById('done_column').innerHTML = '';

    columnsData.todo_column.forEach((cardText,index) => {
        RenderSingleCard(cardText,'todo_column',index);
    });
    columnsData.progress_column.forEach((cardText,index) => {
        RenderSingleCard(cardText,'progress_column',index);
    });
    columnsData.done_column.forEach((cardText,index) => {
        RenderSingleCard(cardText,'done_column',index);
    });
    });
    }






    //Part of main inputs in the main background:
    const AiRequestInput = document.getElementById('ai_request_input');
    const AiStepsPart = document.getElementById('ai_steps_part');
    const GeneratePlanBtn = document.getElementById('generate_plan_btn');


    const CleanPlanBtn = document.getElementById('clean_plan_btn');
    CleanPlanBtn.addEventListener('click', () => {
        AiRequestInput.value = '';
        document.getElementById('generate_plan_btn').innerText = 'Generate';
        AiStepsPart.value = 3;
    });
    AiRequestInput.addEventListener('input', () => {
        const isTooShort = AiRequestInput.value.trim().length < 10;
        GeneratePlanBtn.disabled = isTooShort;
        //console.log('Connecting with ai.....',AiRequestInput.value.trim());
        if (GeneratePlanBtn.disabled) {
            GeneratePlanBtn.classList.add('opacity-75','cursor-not-allowed');
        } else {
            GeneratePlanBtn.classList.remove('opacity-75','cursor-not-allowed');
        }
    });



    const NicknameInput = document.getElementById('nickname_input');
    const EmailInput = document.getElementById('email_input');
    const PasswordInput = document.getElementById('password_input');
    const EmailError = document.getElementById('email_error');
    const SecurityEstimation = document.getElementById('security_estimation');
    const NicknameCheck = document.getElementById('nickname_check');

    const SignUpButton = document.getElementById('sign-up_main_button');
    const SwitchModeBtn = document.getElementById('switch_mode_button');
    const NicknameBlock = document.getElementById('nickname_block');
    let isSignUpMode = true;

    const ForgotPasswordLink = document.getElementById('forgot_password_link');
    const PasswordBlock = PasswordInput.closest('div.flex-col');
    let currentMode = 'sign-up';


    ForgotPasswordLink.addEventListener('click', () => {
    currentMode = 'restore';
    NicknameBlock.classList.add('hidden');
    NicknameInput.classList.add('hidden');
    PasswordBlock.classList.add('hidden');
    ForgotPasswordLink.classList.add('hidden');
    SwitchModeBtn.innerText = 'Sign-in';
    SignUpButton.innerText = 'Send-Code';
    NicknameInput.value = '';
    PasswordInput.value = '';
    SecurityEstimation.classList.add('hidden');
    checkFields();
    });


    SwitchModeBtn.addEventListener('click', () => {
    if (currentMode === 'restore') {
        currentMode = 'sign-in';
    } else if (currentMode === 'sign-up') {
        currentMode = 'sign-in';
    } else {
        currentMode = 'sign-up';
    }

    NicknameInput.value = '';
    EmailInput.value = '';
    PasswordInput.value = '';

    if (currentMode === 'sign-up') {
        NicknameBlock.classList.remove('hidden');
        NicknameInput.classList.remove('hidden');
        PasswordBlock.classList.remove('hidden');
        ForgotPasswordLink.classList.remove('hidden');
        SwitchModeBtn.innerText = 'Sign-in';
        SignUpButton.innerText = 'Sign-up';
    } else if (currentMode === 'sign-in') {
        NicknameBlock.classList.add('hidden');
        NicknameInput.classList.add('hidden');
        PasswordBlock.classList.remove('hidden');
        ForgotPasswordLink.classList.remove('hidden');
        SwitchModeBtn.innerText = 'Sign-up';
        SignUpButton.innerText = 'Sign-in';
    }
    checkFields();
});

    const dependentButton = [
    document.getElementById('sign-up_main_button'),
    ];

    function checkFields() {
        const emailRegex = /^[\w\-.]+@(?:gmail\.com|yandex\.ru)$/;
        const currentEmailValue = EmailInput.value.trim();
        const currentNicknameValue = NicknameInput.value.trim();
        const isPasswordFilled = PasswordInput.value.trim() !== '';
        const isEmailValid = emailRegex.test(EmailInput.value.trim());

        if (currentEmailValue !== '' && !isEmailValid) {
            EmailError.classList.remove('hidden');
        } else {
            EmailError.classList.add('hidden');
        }

        let isNicknameValid = false;
        const nicknameLength = currentNicknameValue.length;
        if (nicknameLength < 3) {
            NicknameCheck.classList.remove('hidden');
        } else {
            NicknameCheck.classList.add('hidden')};
            isNicknameLength = true;

        const currentPasswordValue = PasswordInput.value;
        const hasLetters = /[a-zA-Zа-яА-ЯёЁ]/.test(currentPasswordValue);
        const hasDigits = /[0-9]/.test(currentPasswordValue);
        const passwordLength = currentPasswordValue.length;

        let isPasswordValid = false;
        SecurityEstimation.classList.remove('text-red-400','text-orange-400','text-green-400');
        if (passwordLength === 0) {
            SecurityEstimation.classList.add('hidden');
        } else {
            SecurityEstimation.classList.remove('hidden');
            if (passwordLength < 4) {
                SecurityEstimation.innerText = 'Minimum 4 characters required';
                SecurityEstimation.classList.add('text-red-400');
            }
            else if (passwordLength >= 4 && passwordLength < 6) {
                SecurityEstimation.innerText = 'Weak Password';
                SecurityEstimation.classList.add('text-red-400');

            }
            else if (passwordLength >= 6 && passwordLength < 8) {
                if (hasLetters && hasDigits) {
                    SecurityEstimation.innerText = 'Medium Password';
                    SecurityEstimation.classList.add('text-orange-400');
                    isPasswordValid = true;
                } else {
                    SecurityEstimation.innerText = 'Weak Password';
                    SecurityEstimation.classList.add('text-red-400');
                }
            }
            else if (passwordLength >= 8) {
                if (hasLetters && hasDigits) {
                    SecurityEstimation.innerText = 'Excellent Password';
                    SecurityEstimation.classList.add('text-green-400');
                    isPasswordValid = true;
                } else {
                    SecurityEstimation.innerText = 'Medium Password';
                    SecurityEstimation.classList.add('text-orange-400');
                    isPasswordValid = true;
                }
        }
        }
    dependentButton.forEach(button => {
        if (currentMode === 'sign-up') {
        button.disabled = !(nicknameLength >= 3 && isEmailValid && isPasswordValid);
        } else if (currentMode === 'sign-in') {
        button.disabled = !(isEmailValid && isPasswordValid);
        } else if (currentMode === 'restore') {
        button.disabled = !(isEmailValid);
        }
    });
    }

    NicknameInput.addEventListener('input',checkFields);
    EmailInput.addEventListener('input',checkFields);
    PasswordInput.addEventListener('input',checkFields);

    checkFields();

    function showMainMenu() {
    if (MainBackground && isSettingsOn) {
        document.getElementById('authentication_screen').classList.add('hidden');
        document.getElementById('main_screen').classList.add('hidden');
        document.getElementById('settings_screen').classList.remove('hidden');
        document.getElementById('dashboard_screen').classList.add('hidden');
    } else if (isSettingsOn && !MainBackground) {
        document.getElementById('authentication_screen').classList.add('hidden');
        document.getElementById('main_screen').classList.add('hidden');
        document.getElementById('settings_screen').classList.remove('hidden');
        document.getElementById('dashboard_screen').classList.add('hidden');
    } else if (MainBackground && isBoard) {
        document.getElementById('authentication_screen').classList.add('hidden');
        document.getElementById('settings_screen').classList.add('hidden');
        document.getElementById('main_screen').classList.add('hidden');
        document.getElementById('dashboard_screen').classList.remove('hidden');
    } else if (MainBackground) {
        document.getElementById('authentication_screen').classList.add('hidden');
        document.getElementById('settings_screen').classList.add('hidden');
        document.getElementById('main_screen').classList.remove('hidden');
        document.getElementById('dashboard_screen').classList.add('hidden');
        LoadAndRenderCards();
    }
    else {
        document.getElementById('authentication_screen').classList.remove('hidden');
        document.getElementById('settings_screen').classList.add('hidden');
        document.getElementById('main_screen').classList.add('hidden');
        document.getElementById('dashboard_screen').classList.add('hidden');
    }
    };

    //Part of generate:
    GeneratePlanBtn.addEventListener('click', async () => {
        const taskText = AiRequestInput.value.trim();
        const stepsCount = AiStepsPart.value;
        if (taskText.length < 10) return;

        GeneratePlanBtn.innerText = "Thinking...";
        GeneratePlanBtn.disabled = true;

        const realAISteps = await fetchAIPlan(taskText,stepsCount);
        renderAITasks(realAISteps);

        GeneratePlanBtn.innerText = "Generate";
        GeneratePlanBtn.disabled = false;
        isBoard = true;
        showMainMenu();
    })

    const columns = [TodoColumn,ProgressColumn,DoneColumn];
    columns.forEach(column => {
        //here we permit to drop a card in this column(this is event which tracks card while it is dragged by our mouse)
        column.addEventListener('dragover', (e) => {
            e.preventDefault();
        })
        //here we catch our card
        column.addEventListener('drop', (e) => {
            e.preventDefault();
            //here we get id of our card:
            //previously we put in setData ID of card - now we return it - and we have got the card what we dragged initially
            const id = e.dataTransfer.getData('text/plain');
            //here we get this id
            const draggableCard = document.getElementById(id);
            if (draggableCard) {
            //here another column adopts this card
            column.appendChild(draggableCard);
            updateCounters();
            }
        });
    });

    function updateCounters() {
    document.getElementById('todo_counter').innerText = TodoColumn.children.length;
    document.getElementById('progress_counter').innerText = ProgressColumn.children.length;
    document.getElementById('done_counter').innerText = DoneColumn.children.length;
    }

    //request to AI:

    async function fetchAIPlan(AiRequestInput, AiStepsPart) {
    const apiUrl = "https://polza.ai/api/v1/chat/completions";
    const apiKey = "pza_qoKVZAh0saX6tv2OS7BcRHuGYh3GimYe";

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "google/gemini-3.7-flash",
                messages: [
                    {
                        role: "system",
                        content: `You are a professional task manager. Break down the user's goal into exactly
                        ${AiStepsPart} actionable and sequential steps. You MUST respond ONLY with a raw JSON array of strings,
                        like this: ["Step 1", "Step 2", "Step 3"]. Do not include any introduction, explanations, markdown
                        formatting, or triple backticks. Just the JSON array.`
                    },
                    {
                        role: "user",
                        content: AiRequestInput
                    }
                ],
                temperature: 0.3

            })
        });

        if (!response.ok) throw new Error(`Server Error: ${response.status}`);

        const Data = await response.json();

        const AIResponseText = Data.choices[0].message.content.trim();
        console.log("AI-Response:", AIResponseText);

        const stepsArray = JSON.parse(AIResponseText);
        return stepsArray;

    } catch (error) {
        console.error('Error:', error);
        return [
            "Failed to generate automated plan.",
            "Please check your Groq token or try again.",
            "Verify if the prompt topic is described clearly."
        ];
    }
}

    //Part of the Dashboard:
    const ReturnToMainButtonDashboard = document.getElementById('return_to_main_button2');
    ReturnToMainButtonDashboard.addEventListener('click', () => {
        isBoard = false;
        isSettingsOn = false;
        showMainMenu();
    })

    const DashBoard = document.getElementById('dashboard_button');

    DashBoard.addEventListener('click', () => {
        isSettingsOn = false;
        isBoard = true;
        showMainMenu();
    });


    //part of code of log-out and settings:
    let isSettingsOn = false;
    const SettingsBtn = document.getElementById('settings_button');
    SettingsBtn.addEventListener('click', () => {
    isBoard = false;
    isSettingsOn = true;
    showMainMenu();
    });

    const LogOutBtn = document.getElementById('log-out_button');
    LogOutBtn.addEventListener('click', () => {
    SecurityEstimation.classList.add('hidden');
    NicknameInput.value = '';
    EmailInput.value = '';
    PasswordInput.value = '';
    MainBackground = false;
    isBoard = false;
    isSettingsOn = false;
    showMainMenu();
    });

    const ReturnToMainBtn = document.getElementById('return_to_main_button');
    ReturnToMainBtn.addEventListener('click', () => {
    MainBackground = true;
    isBoard = false;
    isSettingsOn = false;
    showMainMenu();
    });

    //Part of storing the texts of cards:
    SaveCardsBtn = document.getElementById('save_cards_btn');
    DeleteCardsBtn = document.getElementById('delete_cards_btn');
    SaveCardsBtn.addEventListener('click',() => {
        //Here we just gather all cards , but we need to get their innerText
        const todoCards = document.querySelectorAll('#todo_column .my_task_card');
        const progressCards = document.querySelectorAll('#progress_column .my_task_card');
        const doneCards = document.querySelectorAll('#done_column .my_task_card');
        todoText = [];
        progressText = [];
        doneText = [];
        todoCards.forEach(card => {todoText.push(card.innerHTML)});
        progressCards.forEach(card => {progressText.push(card.innerHTML)});
        doneCards.forEach(card => {doneText.push(card.innerHTML)});


        console.log('function sendCardToServer is being prepared to connect Backend');
        console.log("TODO:", todoText);
        fetch('https://cards-hub.website/password_page/save_cards', {
            method: 'POST',
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify({
                user_email: EmailInput.value.trim(),
                todo_column: todoText,
                progress_column: progressText,
                done_column: doneText
            })
        })
    })

    SignUpButton.addEventListener('click',() => {
    if (currentMode === 'sign-up') {
    fetch('https://cards-hub.website/password_page/create_password', {
        method: 'POST',
        headers: {
        'Content-Type' : 'application/json'
        },
        body: JSON.stringify({
            nickname: NicknameInput.value.trim(),
            email: EmailInput.value.trim(),
            password: PasswordInput.value
        })
    })
    .then(res => {
    if (!res.ok) {
        return res.json().then(errData => {
             throw new Error(errData.detail);
        });
    }
    return res.json();
    })
    .then(data => {console.log(data)
    if (data.status_code === 200) {
        alert(data.comment);
        document.getElementById('settings_nickname').innerText = NicknameInput.value.trim();
        document.getElementById('settings_email').innerText = EmailInput.value.trim();
        MainBackground = true;
        showMainMenu();
    }})
    .catch(err =>  {
    console.error(err) ;
    alert("Error: "+ err.message);
    });

    } else if (currentMode === 'sign-in') {
    fetch('https://cards-hub.website/password_page/sign-in', {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify({
            email: EmailInput.value.trim(),
            password: PasswordInput.value
        })
    })
    .then(res => res.json())
    .then(data => {console.log(data);
    if (data.status_code === 200) {
        alert("Hello! " + data.nickname);
        document.getElementById('settings_nickname').innerText = data.nickname;
        document.getElementById('settings_email').innerText = EmailInput.value.trim();
        MainBackground = true;
        showMainMenu();
    } else {
        alert("Error" + (data.detail || "wrong data!"));
    }
    })
    .catch(err => console.error(err));
    } else if (currentMode === 'restore') {
    fetch('https://cards-hub.website/password_page/forgot_password', {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify({
            email: EmailInput.value.trim()
        })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(errData => {
                throw new Error(errData.detail || "Unknown server error");
            });
    }
    return res.json();
    })
    .then(data => {
        console.log(data);
        alert("Code has been sent to email!");
    })
    .catch(err => {
        console.error(err);
        alert("Error: " + err.message);
    });
    }
    });

</script>
</body>
</html>
