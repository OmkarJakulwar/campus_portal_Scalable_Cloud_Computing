const API_BASE_URL = "/api"
let latestCardImageDataUrl = ""
let latestStudentData = null

function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";")
        for (let cookie of cookies) {
            cookie = cookie.trim()
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

function showAlert(id, type, msg) {
    const el = document.getElementById(id)
    if (el) {
        el.innerHTML = `<div class="alert alert-${type}">${msg}</div>`
    }
}

function scrollToRegistration() {
    const registration = document.getElementById("registration")
    if (registration) {
        registration.scrollIntoView({ behavior: "smooth", block: "start" })
    }
}

function setText(id, value) {
    const el = document.getElementById(id)
    if (el) {
        el.textContent = value
    }
}

function showElement(id) {
    const el = document.getElementById(id)
    if (el) {
        el.style.display = "block"
    }
}

function hideElement(id) {
    const el = document.getElementById(id)
    if (el) {
        el.style.display = "none"
    }
}

function addClickHandler(id, handler) {
    const el = document.getElementById(id)
    if (el) {
        el.addEventListener("click", handler)
    }
}

function resetCountryInsightsState() {
    hideElement("countryInsightsLoading")
    hideElement("countryInsightsUnavailable")
    hideElement("countryInsightsCard")

    setText("countryName", "Country")
    setText("countrySubtitle", "Useful relocation insights for the student")
    setText("countryCapital", "N/A")
    setText("countryRegion", "N/A")
    setText("countrySubregion", "N/A")
    setText("countryPopulation", "N/A")
    setText("countryCurrencies", "N/A")
    setText("countryTimezone", "N/A")
    setText("countryLanguages", "N/A")

    const flag = document.getElementById("countryFlag")
    if (flag) {
        flag.style.display = "none"
        flag.src = ""
    }
}

function showStudentInfo(student) {
    const formSection = document.getElementById("registrationFormSection")
    const studentSection = document.getElementById("studentInfoSection")

    const firstName = student.firstName || student.first_name || ""
    const lastName = student.lastName || student.last_name || ""
    const fullName = `${firstName} ${lastName}`.trim() || "N/A"
    const email = student.email || "N/A"
    const phone = student.phone || "N/A"
    const course = student.course || "N/A"
    const homeCountry = student.home_country || student.homeCountry || "N/A"
    const campusCity = student.campus_city || student.campusCity || "N/A"
    const cardId = student.card_id || student.cardId || "N/A"

    latestCardImageDataUrl = student.cardImageDataUrl || ""

    setText("studentInfoName", fullName)
    setText("studentInfoEmail", email)
    setText("studentInfoPhone", phone)
    setText("studentInfoCourse", course)
    setText("studentInfoHomeCountry", homeCountry)
    setText("studentInfoCampusCity", campusCity)
    setText("studentInfoCardId", cardId)

    const downloadBtn = document.getElementById("downloadCardBtn")
    if (downloadBtn) {
        downloadBtn.style.display = latestCardImageDataUrl ? "inline-flex" : "none"
    }

    if (formSection) {
        formSection.style.display = "none"
    }
    if (studentSection) {
        studentSection.style.display = "block"
    }
}

function downloadStudentCard() {
    if (!latestCardImageDataUrl) {
        alert("Card image is not available for download.")
        return
    }

    const cardId = document.getElementById("studentInfoCardId")?.textContent?.trim() || "student-card"
    const link = document.createElement("a")
    link.href = latestCardImageDataUrl
    link.download = `${cardId}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
}

function resetStudentInfo() {
    const formSection = document.getElementById("registrationFormSection")
    const studentSection = document.getElementById("studentInfoSection")
    const registrationForm = document.getElementById("registrationForm")
    const registrationAlert = document.getElementById("registrationAlert")

    latestCardImageDataUrl = ""

    const downloadBtn = document.getElementById("downloadCardBtn")
    if (downloadBtn) {
        downloadBtn.style.display = "none"
    }

    if (formSection) {
        formSection.style.display = "block"
    }
    if (studentSection) {
        studentSection.style.display = "none"
    }
    if (registrationForm) {
        registrationForm.reset()
    }
    if (registrationAlert) {
        registrationAlert.innerHTML = ""
    }

    hideElement("countryInsightsSection")
    resetCountryInsightsState()

    hideElement("restaurantGuideSection")

    const restaurantAlert = document.getElementById("restaurantAlert")
    if (restaurantAlert) {
        restaurantAlert.innerHTML = ""
    }

    const restaurantResults = document.getElementById("restaurantResults")
    const restaurantResultsList = document.getElementById("restaurantResultsList")
    const restaurantResultsEmpty = document.getElementById("restaurantResultsEmpty")

    if (restaurantResults) {
        restaurantResults.classList.add("d-none")
    }
    if (restaurantResultsList) {
        restaurantResultsList.innerHTML = ""
    }
    if (restaurantResultsEmpty) {
        restaurantResultsEmpty.classList.remove("d-none")
    }

    scrollToRegistration()
}

async function showCountryInsights(student) {
    const section = document.getElementById("countryInsightsSection")
    if (!section) return

    const homeCountry = document.getElementById("studentInfoHomeCountry")?.innerText.trim()
    const studentName = `${student.firstName || student.first_name || ""} ${student.lastName || student.last_name || ""}`.trim()

    console.log("Correct country being sent:", homeCountry)
    
    section.style.display = "block"
    resetCountryInsightsState()
    showElement("countryInsightsLoading")

    if (!homeCountry) {
        hideElement("countryInsightsLoading")
        showElement("countryInsightsUnavailable")
        return
    }

    try {
        const resp = await fetch(`${API_BASE_URL}/country-info/?country=${encodeURIComponent(homeCountry)}`)
        const country = await resp.json().catch(() => ({}))

        hideElement("countryInsightsLoading")

        if (!country.success) {
            showElement("countryInsightsUnavailable")
            return
        }

        const currencies = country.currencies
            ? Object.entries(country.currencies)
                .map(([code, value]) => `${code}${value?.name ? ` - ${value.name}` : ""}`)
                .join(", ")
            : "N/A"

        const languages = country.languages
            ? Object.values(country.languages).join(", ")
            : "N/A"

        const timezone = (country.timezones && country.timezones[0]) || "N/A"
        const capital = (country.capital && country.capital[0]) || country.capital || "N/A"
        const region = country.region || "N/A"
        const subregion = country.subregion || "N/A"
        const population = country.population ? Number(country.population).toLocaleString() : "N/A"
        const flagUrl = country.flags?.png || country.flags?.svg || ""

        setText("countryName", country.name || "Country")
        setText("countrySubtitle", `Useful relocation insights for ${studentName || "the student"}`)
        setText("countryCapital", capital)
        setText("countryRegion", region)
        setText("countrySubregion", subregion)
        setText("countryPopulation", population)
        setText("countryCurrencies", currencies)
        setText("countryTimezone", timezone)
        setText("countryLanguages", languages)

        const flag = document.getElementById("countryFlag")
        if (flag && flagUrl) {
            flag.src = flagUrl
            flag.alt = `${country.name || "Country"} flag`
            flag.style.display = "block"
        }

        showElement("countryInsightsCard")
    } catch (err) {
        console.error("Country API error", err)
        hideElement("countryInsightsLoading")
        showElement("countryInsightsUnavailable")
    }
}

function showRestaurantAlert(type, msg) {
    const alertBox = document.getElementById("restaurantAlert")
    if (alertBox) {
        alertBox.innerHTML = `<div class="alert alert-${type}">${msg}</div>`
    }
}

function createRestaurantCard(restaurant) {
    const col = document.createElement("div")
    col.className = "col-12"

    const card = document.createElement("div")
    card.className = "profile-card h-100"

    const title = document.createElement("h4")
    title.innerHTML = `<i class="bi bi-shop"></i> ${restaurant.name || "Unnamed Restaurant"}`

    const location = document.createElement("p")
    location.innerHTML = `<strong>Location:</strong> ${restaurant.location || "N/A"}`

    const cuisine = document.createElement("p")
    cuisine.innerHTML = `<strong>Cuisine:</strong> ${restaurant.cuisine || "N/A"}`

    const rating = document.createElement("p")
    rating.innerHTML = `<strong>Rating:</strong> ${restaurant.rating ?? "N/A"}`

    const price = document.createElement("p")
    price.innerHTML = `<strong>Price Level:</strong> ${restaurant.price_level ?? "N/A"}`

    const coordinates = document.createElement("p")
    coordinates.innerHTML = `<strong>Coordinates:</strong> ${restaurant.latitude ?? "N/A"}, ${restaurant.longitude ?? "N/A"}`

    card.appendChild(title)
    card.appendChild(location)
    card.appendChild(cuisine)
    card.appendChild(rating)
    card.appendChild(price)
    card.appendChild(coordinates)

    col.appendChild(card)
    return col
}

function renderRestaurantResults(restaurants) {
    const resultsBox = document.getElementById("restaurantResults")
    const resultsList = document.getElementById("restaurantResultsList")
    const emptyState = document.getElementById("restaurantResultsEmpty")

    if (!resultsBox || !resultsList || !emptyState) return

    resultsList.innerHTML = ""

    if (!restaurants || restaurants.length === 0) {
        resultsBox.classList.add("d-none")
        emptyState.classList.remove("d-none")
        emptyState.textContent = "No restaurant recommendations found for the selected preferences."
        return
    }

    restaurants.forEach((restaurant) => {
        resultsList.appendChild(createRestaurantCard(restaurant))
    })

    emptyState.classList.add("d-none")
    resultsBox.classList.remove("d-none")
}

addClickHandler("downloadCardBtn", () => {
    downloadStudentCard()
})

addClickHandler("nav-registration", (e) => {
    e.preventDefault()
    scrollToRegistration()
})

addClickHandler("nav-registration-quick", (e) => {
    e.preventDefault()
    scrollToRegistration()
})

addClickHandler("openCountryInsights", (e) => {
    e.preventDefault()
    const section = document.getElementById("countryInsightsSection")
    if (section) {
        section.style.display = "block"
        section.scrollIntoView({ behavior: "smooth", block: "start" })
    }
})

addClickHandler("openRestaurantGuide", (e) => {
    e.preventDefault()

    const restaurantGuideSection = document.getElementById("restaurantGuideSection")
    if (restaurantGuideSection) {
        restaurantGuideSection.style.display = "block"
        restaurantGuideSection.scrollIntoView({ behavior: "smooth", block: "start" })
    }

    const cityInput = document.getElementById("city")
    const restaurantCityInput = document.getElementById("restaurantCity")
    if (cityInput && restaurantCityInput && cityInput.value.trim() && !restaurantCityInput.value.trim()) {
        restaurantCityInput.value = cityInput.value.trim()
    }
})

addClickHandler("openWelcomePack", (e) => {
    e.preventDefault()
    const section = document.getElementById("welcomePackSection")
    if (section) {
        section.style.display = "block"
        section.scrollIntoView({ behavior: "smooth", block: "start" })
    }
})

addClickHandler("generateWelcomePackBtn", async () => {
    if (!latestStudentData || !latestStudentData.id) {
        showWelcomePackAlert("warning", "Please register a student first.")
        return
    }

    showWelcomePackAlert("info", "Generating welcome pack...")

    try {
        const response = await fetch(`${API_BASE_URL}/generate-welcome-pack/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                student_id: latestStudentData.id
            })
        })

        const data = await response.json().catch(() => ({}))

        if (response.ok) {
            showWelcomePackAlert("success", "Welcome pack generation started successfully.")

            let countryData = null
            let restaurants = []

            try {
                const countryResp = await fetch(
                    `${API_BASE_URL}/country-info/?country=${encodeURIComponent(latestStudentData.home_country || "")}`
                )
                countryData = await countryResp.json().catch(() => null)
            } catch (e) {
                console.error("Country fetch for welcome pack failed", e)
            }

            try {
                const restaurantResp = await fetch(`${API_BASE_URL}/get-restaurants/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({
                        city: latestStudentData.campus_city || "",
                        cuisine: "Indian",
                        budget: 2,
                        min_rating: 4
                    })
                })

                const restaurantData = await restaurantResp.json().catch(() => ({}))
                restaurants = restaurantData.restaurants || []
            } catch (e) {
                console.error("Restaurant fetch for welcome pack failed", e)
            }

            renderWelcomePack(latestStudentData, countryData, restaurants)
        } else {
            showWelcomePackAlert("danger", data.error || "Failed to generate welcome pack.")
        }
    } catch (error) {
        showWelcomePackAlert("danger", error.message)
    }
})

const registrationForm = document.getElementById("registrationForm")
if (registrationForm) {
    registrationForm.addEventListener("submit", async (e) => {
        e.preventDefault()

        const formData = {
            firstName: document.getElementById("firstName")?.value.trim(),
            lastName: document.getElementById("lastName")?.value.trim(),
            email: document.getElementById("email")?.value.trim(),
            phone: document.getElementById("phone")?.value.trim(),
            home_country: document.getElementById("country")?.value.trim(),
            campus_city: document.getElementById("city")?.value.trim(),
            course: document.getElementById("course")?.value.trim()
        }

        try {
            const res = await fetch(`${API_BASE_URL}/register-student/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(formData)
            })

            const data = await res.json().catch(() => ({}))

            if (res.ok) {
                latestStudentData = data
                showAlert("registrationAlert", "success", "Registration successful!")
                showStudentInfo(data)
                await showCountryInsights(data)

                const studentInfoSection = document.getElementById("studentInfoSection")
                if (studentInfoSection) {
                    studentInfoSection.scrollIntoView({ behavior: "smooth", block: "start" })
                }
            } else {
                showAlert(
                    "registrationAlert",
                    "danger",
                    `Registration error: "Error ! please try again later."`
                )
            }
        } catch (err) {
            showAlert("registrationAlert", "danger", err.message)
        }
    })
}

const restaurantForm = document.getElementById("restaurantForm")
if (restaurantForm) {
    restaurantForm.addEventListener("submit", async (e) => {
        e.preventDefault()

        const payload = {
            city: document.getElementById("restaurantCity")?.value.trim(),
            cuisine: document.getElementById("restaurantCuisine")?.value.trim(),
            budget: document.getElementById("restaurantBudget")?.value.trim(),
            min_rating: document.getElementById("restaurantRating")?.value.trim()
        }

        if (!payload.city) {
            showRestaurantAlert("danger", "City is required.")
            return
        }

        try {
            const response = await fetch(`${API_BASE_URL}/get-restaurants/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(payload)
            })

            const data = await response.json().catch(() => ({}))

            if (response.ok && data.success) {
                showRestaurantAlert("success", "Restaurant recommendations loaded successfully.")
                renderRestaurantResults(data.restaurants)
            } else {
                showRestaurantAlert("danger", data.error || "Failed to fetch restaurant recommendations.")
                renderRestaurantResults([])
            }
        } catch (error) {
            showRestaurantAlert("danger", error.message)
            renderRestaurantResults([])
        }
    })
}

function showWelcomePackAlert(type, msg) {
    const alertBox = document.getElementById("welcomePackAlert")
    if (alertBox) {
        alertBox.innerHTML = `<div class="alert alert-${type}">${msg}</div>`
    }
}

function renderWelcomePack(student, countryData = null, restaurants = []) {
    const content = document.getElementById("welcomePackContent")
    if (!content || !student) return

    const fullName = `${student.firstName || student.first_name || ""} ${student.lastName || student.last_name || ""}`.trim() || "N/A"
    const cardId = student.card_id || student.cardId || "N/A"
    const course = student.course || "N/A"
    const campusCity = student.campus_city || student.campusCity || "N/A"
    const homeCountry = student.home_country || student.homeCountry || "N/A"

    let countryHtml = `<p><strong>Country Information:</strong> Not available</p>`
    if (countryData && countryData.success) {
        const currencies = countryData.currencies
            ? Object.keys(countryData.currencies).join(", ")
            : "N/A"

        countryHtml = `
            <p><strong>Country:</strong> ${countryData.name || "N/A"}</p>
            <p><strong>Currency:</strong> ${currencies}</p>
            <p><strong>Timezone:</strong> ${(countryData.timezones && countryData.timezones[0]) || "N/A"}</p>
        `
    }

    let restaurantHtml = `<p>No restaurant recommendations available.</p>`
    if (restaurants && restaurants.length > 0) {
        restaurantHtml = `
            <ul class="mb-0">
                ${restaurants.slice(0, 3).map(r => `
                    <li>${r.name || "Restaurant"} - ${r.cuisine || "N/A"} (${r.rating ?? "N/A"})</li>
                `).join("")}
            </ul>
        `
    }

    content.innerHTML = `
        <div class="profile-card mb-0">
            <h4><i class="bi bi-stars"></i> Student Welcome Pack</h4>
            <p><strong>Name:</strong> ${fullName}</p>
            <p><strong>Course:</strong> ${course}</p>
            <p><strong>Campus City:</strong> ${campusCity}</p>
            <p><strong>Home Country:</strong> ${homeCountry}</p>
            <p><strong>Card ID:</strong> <span class="badge bg-success">${cardId}</span></p>

            <hr>

            <h5>Country Insights</h5>
            ${countryHtml}

            <hr>

            <h5>Recommended Restaurants</h5>
            ${restaurantHtml}

            <hr>

            <h5>Welcome Note</h5>
            <p>
                Welcome to your student onboarding journey. Use this portal to explore country insights,
                local recommendations, and prepare for life in your campus city.
            </p>
        </div>
    `
}