describe('Todo functionality', () => {
    // define variables that we need on multiple occasions
  let uid // user id
  let name // email of the user
  let email // name of the user (firstName + ' ' + lastName)

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid
        name = user.firstName + ' ' + user.lastName
        email = user.email
      })
    })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')

    // login div 
    cy.contains('div', 'Email Address')
    // Hittar textrutan just i det div:et och skriver in emailen
      .find('input[type=text]')
      .type(email)

      // hittar formuläret och skickar in det
    cy.get('form').submit()

    // säkerställ att vi är inne
    cy.get('h1')
      .should('contain.text', 'Your tasks')

    // skapa task (exakt enligt TaskCreator.js)
    // # är id-selektorn i CSS, så #title betyder "elementet med id title"
    cy.get('#title').type('Test task')
    cy.get('#url').type('abc123')

    // knapp som skapar tasken som inte är button
    // knappen är disabled så länge title är tom, så säkerställ att den inte är det innan vi klickar
    cy.get('input[type="submit"]')
      .should('not.be.disabled')
      .click()

    // öppna task
    cy.contains('Test task').click()
  })

    it('should add a new todo', () => {
        // hitta textrutan för att lägga till en ny todo, skriv in "my first todo" och klicka på "Add"
        // TaskCreator.js har en textruta med placeholder "Add a new todo item", så vi kan hitta den textrutan genom att leta efter den placeholder-texten
    cy.get('input[placeholder="Add a new todo item"]')
        .scrollIntoView()
        .type('my first todo', { force: true })

        // add-knappen är av typen submit, så vi kan hitta den genom att leta efter input-elementet med type submit
    cy.get('.inline-form input[type="submit"]')
    // klicka ändå, fast Cypress tycker den är dold 
        .click({ force: true })

        // kontrollera att "my first todo" nu finns på sidan
    cy.contains('my first todo')
        .should('exist')
    })

    it('should toggle a todo', () => {
        cy.contains('Watch video')
        // föräldrarna till "Watch video" har en div med class "checker" som är en custom checkbox, så hitta den och klicka på den
            .parent()
            // hittar i TaskDetail.js
            .find('.checker')
            .click()

        cy.contains('Watch video')
            .parent()
            .find('.checker')
            // efter att ha klickat på checkboxen så ska den ha klassen "checked", så kontrollera det
            .should('have.class', 'checked')
    })

    it('should delete a todo', () => {
      cy.contains('Watch video')
        .parent()
        .find('.remover')
        .click()

      cy.contains('Watch video')
        .should('not.exist')
    })

    // after(function () {
    //     // clean up by deleting the user from the database
    //     cy.request({
    //         method: 'DELETE',
    //         url: `http://localhost:5000/users/${uid}`
    //     }).then((response) => {
    //         cy.log(response.body)
    //     })
    // })
})