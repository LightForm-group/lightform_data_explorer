function clear_select(select_element) {
    // Remove all current options from a HTML select element
    for (let a in select_element.options) {
        select_element.options.remove(0);
    }
}

function activate_select_option(select_element, name) {
    // Change the selectedIndex of a select element to the index of the option with text = `name`.
    // If name is not found in the options then do not change the selection.
    for (let i = 0; i < select_element.length; i++) {
        if (select_element[i].text === name) {
            select_element.selectedIndex = i
            break
        }
    }
}

function remember_active_tab(default_tab_id) {
    // Script to set active bootstrap tab on page reload.
    let activePage = sessionStorage.getItem('activePage')
    let activeTab = sessionStorage.getItem('activeTab')
    if (activePage === document.URL && activeTab) {
        new bootstrap.Tab(document.querySelector(`#${activeTab}`)).show()
        }
    else {
        new bootstrap.Tab(document.querySelector(`#${default_tab_id}`)).show()
    }

    document.addEventListener("shown.bs.tab", function (e) {
        sessionStorage.setItem('activeTab', e.target.id)
        sessionStorage.setItem('activePage', document.URL)
    })
}
