
function setSlideImage() {

    let imageDots = document.querySelectorAll(".slideDotes");

    imageDots.forEach((element, index) => {
        element.addEventListener("click", (event) => {
            let headShowcase = document.querySelector(".SlideImages");
            headShowcase.style.backgroundImage = `url("media/HeadShowcase/${index + 1}.jpg")`;
            imageDots.forEach(el => el.classList.remove("Activedot"));
            element.classList.add("Activedot");
        })
    });

    function autoSlide(index) {
        imageDots.forEach(el => el.classList.remove("Activedot"));
        imageDots[index - 1].classList.add("Activedot");
        let headShowcase = document.querySelector(".SlideImages");
        headShowcase.style.backgroundImage = `url("media/HeadShowcase/${index}.jpg")`;
        (index < 5) ? index++ : index = 1;
        setTimeout(() => autoSlide(index), 4000);
    }

    autoSlide(1);
}


function setPagination() {
    let pageNumbers = document.querySelectorAll(".PageNumber > a");
    let url = new URL(window.location.href);
    let page = url.searchParams.get("page");
    let nextPage = document.querySelector("#NextPage");
    let previousPage = document.querySelector("#PreviousPage");

    if (page === null) {
        page = 1;
    }

    let pageCopy = page;
    pageNumbers.forEach((element, num) => {
        element.textContent = pageCopy;
        let cat = url.searchParams.get("category");
        if (cat)
            element.href = `?category=${cat}` + `&page=${pageCopy}`;
        else
            element.href = `?page=${pageCopy}`;

        pageCopy++;
    });

    nextPage.href = `?page=${parseInt(page) + 1}`;
    previousPage.href = `?page=${parseInt(page) - 1}`;
}


function setCategory() {
    let url = new URL(window.location.href);
    let category = url.searchParams.get("category");
    let categoryTabs = document.querySelectorAll(".CategoryIndex > a");

    if (category) {
        categoryTabs.forEach((element) => {
            if (element.textContent.trim() === category.trim()) {
                categoryTabs[0].id = "";
                element.id = "ActiveCategoryIndex";
            }
        })
    }

}

function setSearchPaging(){
    let url = new URL(window.location.href);
    let query = url.searchParams.get("q");
    let pageNumbers = document.querySelectorAll(".PageNumber > a");

    if(query){

        pageNumbers.forEach((element)=>{
            element.href = `?q=${query}` + `&page=${element.textContent}`;
        })

    }
}

// Run Functions
setSlideImage();
setCategory();
setPagination();
setSearchPaging();
