



document.addEventListener('DOMContentLoaded', function(){
  var element = document.querySelector('#container')
  panzoom(element)
  
    }

  )


    
// The list will contain all stars that could be unlocked but currently are not.
let possibleToUnlock = []
// Divs with this classname should only be visible on hover.
$('.toDisplayOnHover').hide()
$('.starContainer').hover(DisplayAttributesWindow)
$('.starName, .attributes, .affinityRequirement, .affinityBonus').on('mouseenter', function (){
  $('.toDisplayOnHover').hide()
})
  function DisplayAttributesWindow() {
    const hoveredItem = $(this)[0].classList[1]
    $.ajax({
      type : 'POST',
      url : displayAttrUrl,
      data: {'data': hoveredItem}
    }).done(function() {
      $.getJSON(displayAttrUrl, function(data) {
        $('.toDisplayOnHover.' + hoveredItem).toggle()
        // This block of code makes sure that star names are displayed correctly.
        let name = document.querySelector('.toDisplayOnHover.' + hoveredItem + ' p')
        let textName = name.textContent
        let particularName = data.result.pop() 
        if (textName.indexOf(particularName) == -1){
          text = name.textContent
          let nameNode = document.createTextNode(particularName)
          name.insertBefore(nameNode, name.childNodes[0])
        }
        // Now create paragraphs meant for attributes.
        let attr = document.querySelector('.attributes.' + hoveredItem)
        let attributeText = attr.textContent
        let standardDone = false
        let counter = 0
        let attributesTitle;
        let abilitiesTitle;
        let specificDisplayed = false
        let specificTwoDisplayed = false 
        let secondSkillTitle;
        if (attributeText.length == 0){
          data.result.forEach(function(x){
            counter += 1
            if (counter === data.result.length){
              standardDone = true
            }
            if (x.indexOf('Attributes') !== -1){
              attributesTitle = x
            }
            if (x.indexOf('Abilities') !== -1){
              abilitiesTitle = x
            }
            if (x.indexOf('specific') !== -1){
              skillTitle = x
              skillTitle = skillTitle.replace('specific', '')
            }
            if (x.indexOf('particular') !== -1){
              secondSkillTitle = x
              secondSkillTitle = secondSkillTitle.replace('particular', '')
            }
            // Leave pets attributes and skills till last so that they are displayed below the main chain of attributes.
            if (x.indexOf('pets') !== -1 || x.indexOf('attr') !== -1 || x.indexOf('abl') !== -1 || x.indexOf('skl') !== -1 || x.indexOf('Attributes') !== -1|| x.indexOf('Abilities') !== -1 || x.indexOf('specific') !== -1 || x.indexOf('particular') !== -1 || x.indexOf('acv') !== -1){ return; }
            let toAppend = ''
            toAppend = x + "<br>"
            $(attr).append(toAppend)
          })
        if (standardDone === true){      
          data.result.forEach(function(x){        
            if (x.indexOf('pets') !== -1){
              x = x.replace('pets', '')
              if (attr.textContent.indexOf('Bonus') === -1){
                  $(attr).append("<br>" + 'Bonus to All Pets' + "<br>" + x )
              }else{
                $(attr).append("<br>" + x)
              }
            }else if (x.indexOf('attr') !== -1){
              x = x.replace('attr', '')
              if (attr.textContent.indexOf('Attributes') === -1){
                $(attr).append("<br>" + attributesTitle + "<br>" + x )
              }else{
                $(attr).append("<br>" + x)
              }
            }else if(x.indexOf('abl') !== -1){         
              x = x.replace('abl', '')
              if (attr.textContent.indexOf('Abilities') === -1){
                $(attr).append("<br>" + "<br>" + abilitiesTitle + "<br>" + x )
              }else{
                $(attr).append("<br>" + x)
              }
            }else if(x.indexOf('skl') !== -1){
              x = x.replace('skl', '')
              if (attr.textContent.indexOf('specific') === -1 && specificDisplayed === false){            
                $(attr).append("<br>" + "<br>" + skillTitle + "<br>" + x )
                specificDisplayed = true
              }else{
                $(attr).append("<br>" + x)
              }
            }else if(x.indexOf('acv') !== -1){
              x = x.replace('acv', '')
              if (attr.textContent.indexOf('particular') === -1 && specificTwoDisplayed === false){           
                $(attr).append("<br>" + "<br>" + secondSkillTitle + "<br>" + x )
                specificTwoDisplayed = true
              }else{
                $(attr).append("<br>" + x )
              }
            }
          })
        }
        }
        // Display requirements for a star.
        let requirement = document.querySelector('.affinityRequirement.' + hoveredItem)
        if (requirement.getElementsByTagName('img').length == 0){
          if (data.first_affinity.indexOf('Primordial') != -1){
            $(requirement).append(primordialUrl + data.first_affinity_value.toString() + "<br>")
            
          }
          if (data.first_affinity.indexOf('Ascendant') != -1){
            $(requirement).append(ascendantsUrl + data.first_affinity_value.toString() + "<br>")
          }
          if (data.first_affinity.indexOf('Eldritch') != -1){
            $(requirement).append(eldritchUrl + data.first_affinity_value.toString() + "<br>")
          }
          if (data.first_affinity.indexOf('Chaos') != -1){
            $(requirement).append(chaosUrl + data.first_affinity_value.toString() + "<br>")
          }
          if (data.first_affinity.indexOf('Order') != -1){
            $(requirement).append(orderUrl + data.first_affinity_value.toString() + "<br>")
          }
          if (data.second_affinity !== null){
            if (data.second_affinity.indexOf('Primordial') != -1){
              $(requirement).append(primordialUrl + data.second_affinity_value.toString() + "<br>")
            }
            if (data.second_affinity.indexOf('Ascendant') != -1){
              $(requirement).append(ascendantsUrl + data.second_affinity_value.toString() + "<br>")
            }
            if (data.second_affinity.indexOf('Eldritch') != -1){
              $(requirement).append(eldritchUrl + data.second_affinity_value.toString() + "<br>")
            }
            if (data.second_affinity.indexOf('Chaos') != -1){
              $(requirement).append(chaosUrl + data.second_affinity_value.toString() + "<br>")
            }
            if (data.second_affinity.indexOf('Order') != -1){
              $(requirement).append(orderUrl + data.second_affinity_value.toString() + "<br>")
            }
          }
          if (data.third_affinity !== null){
            if (data.third_affinity.indexOf('Primordial') != -1){
              $(requirement).append(primordialUrl + data.third_affinity_value.toString() + "<br>")
            }
            if (data.third_affinity.indexOf('Ascendant') != -1){
              $(requirement).append(ascendantsUrl + data.third_affinity_value.toString() + "<br>")
            }
            if (data.third_affinity.indexOf('Eldritch') != -1){
              $(requirement).append(eldritchUrl + data.third_affinity_value.toString() + "<br>")
            }
            if (data.third_affinity.indexOf('Chaos') != -1){
              $(requirement).append(chaosUrl + data.third_affinity_value.toString() + "<br>")
            }
            if (data.third_affinity.indexOf('Order') != -1){
              $(requirement).append(orderUrl + data.third_affinity_value.toString() + "<br>")
            }
          }
          // Display affinity bonuses of a star.
          let bonus = document.querySelector('.affinityBonus.' + hoveredItem)
          if (data.first_bonus !== null && data.first_bonus !== 'no affinity bonus'){
    
            if (data.first_bonus.indexOf('Primordial') != -1){
              $(bonus).append(primordialUrl + data.first_bonus_value.toString() + "<br>")
            }
            if (data.first_bonus.indexOf('Ascendant') != -1){
              $(bonus).append(ascendantsUrl + data.first_bonus_value.toString() + "<br>")
            }
            if (data.first_bonus.indexOf('Eldritch') != -1){
              $(bonus).append(eldritchUrl + data.first_bonus_value.toString() + "<br>")
            }
            if (data.first_bonus.indexOf('Chaos') != -1){
              $(bonus).append(chaosUrl + data.first_bonus_value.toString() + "<br>")
            }
            if (data.first_bonus.indexOf('Order') != -1){
              $(bonus).append(orderUrl + data.first_bonus_value.toString() + "<br>")
            }
    
          }else{
            $(bonus).remove()
          }
    
          if (data.second_bonus !== null){
    
            if (data.second_bonus.indexOf('Primordial') != -1){
              $(bonus).append(primordialUrl + data.second_bonus_value.toString())
    
            }
            if (data.second_bonus.indexOf('Ascendant') != -1){
              $(bonus).append(ascendantsUrl + data.second_bonus_value.toString())
    
            }
            if (data.second_bonus.indexOf('Eldritch') != -1){
              $(bonus).append(eldritchUrl + data.second_bonus_value.toString())
    
            }
            if (data.second_bonus.indexOf('Chaos') != -1){
              $(bonus).append(chaosUrl + data.second_bonus_value.toString())
    
            }
            if (data.second_bonus.indexOf('Order') != -1){
              $(bonus).append(orderUrl + data.second_bonus_value.toString())
    
            }
        }
        }
        })
      })
    }

// List of stars' ids will be compared against a list of unlocked stars fetched from the server. The stars present in both lists will change its appearance. 
const idsAndObjects = $('.starContainer').toArray()
const idsList = idsAndObjects.map(function(element){
  return element.id
});
// Blink mode activates execution of backend function fast_mode.
function activateBlinkMode() {
  const clickedItem = $(this)[0].classList[1]
  $.ajax({
    type : 'POST',
    url : blinkUrl,
    data: {clickedItem:clickedItem},
    traditional: true
  }).done(function(){
    $.getJSON(blinkUrl, function(data) {
      let intersection = data.result.filter(element => idsList.includes(element));
      intersection.forEach(function(item){
        // If a star is present in both lists, change its background picture so that it is perceived as unlocked.
        $('.starContainer#' + item).css({'background-image': starDownUrl, 'mix-blend-mode': 'lighten'})
        possibleToUnlock.push(item)
        // Update affinity counters.
        $('#ascendantsCounter p').html(data.asc)
        $('#chaosCounter p').html(data.chs)
        $('#eldritchCounter p').html(data.eld)
        $('#orderCounter p').html(data.ord)
        $('#primordialCounter p').html(data.prim)
        $('#devotionAvailable').html(data.devpoints)
        // Check which stars could be unlocked and mark them with glowing effect.
      let matchings = data.to_glow.filter(element => idsList.includes(element));
      matchings.forEach(function(item){
        let imageBackground = $('.starContainer#' + item).css('background')
        if (imageBackground.indexOf('devotion_star_skill') === -1){
          let starGlow = $('.starContainer#' + item).css('background-image', starOverUrl)
        } 
      })
      })
      });
  })
  }
// The basic control flow of buttons and functions which they trigger. For example, once a blinkMode is clicked, the second click on the button should be disabled to avoid potential bugs.
$('.blinkMode').bind('click', function(){
  $('.blinkMode').css({'color': 'green', 'background-color': 'lightgreen'})
  $('.standardMode').css({'color': 'black', 'background-color': '#9BABA8'})
  $('.starContainer').bind('click', activateBlinkMode)
  $('.blinkMode').prop('disabled', true)
  $('.standardMode').prop('disabled', false)
  $('.starContainer').off('click', activateStandardMode)
})
$('.standardMode').bind('click', function(){ 
    $('.starContainer').off('click', activateBlinkMode)
    $('.blinkMode').css({'color': 'black', 'background-color': '#9BABA8'})
    $('.standardMode').css({'color': 'green', 'background-color': 'lightgreen'})
    $('.starContainer').bind('click', activateStandardMode)
    $('.starContainer').contextmenu(standardModeLock)
    $('.standardMode').prop('disabled', true);
    $('.blinkMode').prop('disabled', false);
})
$('.resultsButton').on('click', displayResults)
$('.results').hide();
// InnerButton appears when results window opens and is used to close it.
$('#innerButton').on('click', function(){
$('.results').hide();
$('.resultsButton').toggle();
})

// The reset function not only resets devotion points to its default value, it is also responsible for reseting stars' appearences to the initial, disabled state.
$(function(){
  $('#reset').bind('click', function(){
    $.ajax({
      type:'POST',
      url: resetUrl
    }).done(function(){
      $.getJSON(resetUrl, function(data){
        if(data.result.length === 0){
          $('.starContainer').css('background-image', starDisabledUrl)
          $('.starContainer.skill').css('background-image', starSkillUrl)
          $('#devotionAvailable').html(data.devpoints)
          $('#ascendantsCounter p').html(data.asc)
          $('#chaosCounter p').html(data.chs)
          $('#eldritchCounter p').html(data.eld)
          $('#orderCounter p').html(data.ord)
          $('#primordialCounter p').html(data.prim)
        }
      })
    })
  })
})
// The below variable is going to store the value of a background-image of a given star.
let imageString;
// Swap the background picture of a hovered star to add a glowing effect. It has to be done using JS because css ':hover' does not work once the 'background' attribute is changed via JS(after the reset function is executed). 
$('.starContainer').mouseenter(function(){
  imageString = $(this).css('background-image')
  // Change the background image only if the hovered star is not unlocked and cannot be unlocked.
  if (imageString.indexOf('devotion_star_disabled') !== -1){
    $(this).css('background-image', starGlowUrl)
  // Use a different animation if the hovered star is unlocked.
  }else if (imageString.indexOf('devotion_star_down') !== -1){
    $(this).css('background-image', downGlowUrl)
    // $(this).css('background-image', "url('static/styles/devotion_star_downglow.png')")
  // Use a different animation if the hovered star can be unlocked.
  }else if (imageString.indexOf('devotion_star_overs') !== -1){
    $(this).css('background-image', skillTwoUrl)
    // $(this).css('background-image', "url('static/styles/devotion_star_over2.png')")
  }   
})
// Change the background image to the animation unique to the stars which grant skills.
$('.starContainer.skill').mouseenter(function(){
  imageString = $(this).css('background-image')
  // Keep the current background image if it is 'star_down'.
  if (imageString.indexOf('devotion_star_down') !== -1){
    return;
  // Use different animation if the star background is not 'down'.
  }else{
    $(this).css('background-image', skillGlowUrl)
    // $(this).css('background-image', "url('static/styles/devotion_star_skillglow.png')")
  }
  
})
$('.starContainer.skill').mouseleave(function(){
  imageString = $(this).css('background-image')
  // Keep the current background image if it is 'star_down'.
  if (imageString.indexOf('devotion_star_down') > -1){
    return;   
  // Use different animation if the star background is not 'down'.  
  }else{
    $(this).css('background-image', starSkillUrl)
    // $(this).css('background-image', "url('static/styles/devotion_star_skill.png')")
  }
})
// Change the background image back to the original one.
$('.starContainer').mouseleave(function(){
  imageString = $(this).css('background-image')
  if (imageString.indexOf('devotion_starglow01') !== -1){
    $(this).css('background-image', starDisabledUrl)
    // $(this).css('background-image', "url('static/styles/devotion_star_disabled.png')")
  }else if (imageString.indexOf('devotion_star_downglow') !== -1){
    $(this).css('background-image', starDownUrl)
    // $(this).css('background-image', "url('static/styles/devotion_star_down.png')")
  }else if (imageString.indexOf('devotion_star_over2') !== -1){
    $(this).css('background-image', starOverUrl)
    // $(this).css('background-image', "url('static/styles/devotion_star_overs.png')")
  }  
})
// Activate backend function which unlocks stars in the standard way, known from the game.
function activateStandardMode() {  
  const clickedItem = $(this)[0].classList[1]
  const itemId = this.id
  let imageString = $('.starContainer#' + itemId).css('background-image')
  let standardDone = false
  // Prevent the function execution if the clicked star has already been unlocked.
  if (imageString.indexOf('devotion_star_down') === -1){
    $.ajax({
    type : 'POST',
    url : standardUrl,
    data: {'data': clickedItem}
  }).done(function() {
    $.getJSON(standardUrl, function(data) {
// The result True means that the clicked star was successfully unlocked.
      if (data.result === true) {
        $('.starContainer#' + itemId).css('background-image', starDownUrl)
        // Update affinity counters.
        $('#ascendantsCounter p').html(data.asc)
        $('#chaosCounter p').html(data.chs)
        $('#eldritchCounter p').html(data.eld)
        $('#orderCounter p').html(data.ord)
        $('#primordialCounter p').html(data.prim)
        $('#devotionAvailable').html(data.devpoints)
        // Add a glowing effect to stars which could be unlocked.
        let matchings = data.to_glow.filter(element => idsList.includes(element));
      matchings.forEach(function(item){
        let imageBackground = $('.starContainer#' + item).css('background')
        if (imageBackground.indexOf('devotion_star_skill') === -1){
          let starGlow = $('.starContainer#' + item).css('background-image', starOverUrl)
          if (possibleToUnlock.includes(item) === false){
            possibleToUnlock.push(item)       
          }         
        }        
      })
      }     
    })
  })
  }  
}
// Activate backend function which locks stars in the standard way, known from the game.
function standardModeLock() {
  const clickedItem = $(this)[0].classList[1]
  const itemId = this.id
  let imageString = $('.starContainer#' + itemId).css('background-image')
  if (imageString.indexOf('devotion_star_down') !== -1){
    $.ajax({
    type : 'POST',
    url : standardLockUrl,
    data: {'data': clickedItem}
  }).done(function() {
    // Result False means that the star has been successfully locked(is not present in the data.result array).
    $.getJSON(standardLockUrl, function(data) {
      if (data.result === false) {  
        // Update affinity counters.     
        $('#ascendantsCounter p').html(data.asc)
        $('#chaosCounter p').html(data.chs)
        $('#eldritchCounter p').html(data.eld)
        $('#orderCounter p').html(data.ord)
        $('#primordialCounter p').html(data.prim)
        $('#devotionAvailable').html(data.devpoints)
        // Add a glowing effect to stars which could be unlocked.
        let matchings = data.to_glow.filter(element => idsList.includes(element));
        if (matchings.includes(itemId)){
          $('.starContainer#' + itemId).css('background-image', starOverUrl)
        }
      matchings.forEach(function(item){
        let imageBackground = $('.starContainer#' + item).css('background')    
        possibleToUnlock[possibleToUnlock.indexOf(item)] = undefined
        
      })
      possibleToUnlock.forEach(function(element){
        if (typeof element !== 'undefined'){
          if ($('.starContainer#' + element).css('background-image').indexOf('devotion_star_down') === -1){
          $('.starContainer#' + element).css('background-image', starDisabledUrl)
        }
        }
        
        
      })
      possibleToUnlock = []
      possibleToUnlock = [...matchings]
      }
      
    })
  })
  }
}
// The third-sixth column must be initially hidden. Once there are enough results to display, more columns will be shown.
$('#thirdColumn p').toggle()
$('#fourthColumn p').toggle()
$('#fifthColumn p').toggle()
$('#sixthColumn p').toggle()

// Display all gained bonuses in the results window.
function displayResults(){
  $('.results').toggle()
  $('.resultsButton').css('display', 'none')
  let firstColumn = document.querySelector('#firstColumn p')
  let secondColumn = document.querySelector('#secondColumn p')
  let thirdColumn = document.querySelector('#thirdColumn p')
  let fourthColumn = document.querySelector('#fourthColumn p')
  let fifthColumn = document.querySelector('#fifthColumn p')
  let sixthColumn = document.querySelector('#sixthColumn p')
  let paragraphCounter = 0
  $.getJSON(resultsUrl, function(data){
    // Delete any existing text content so that it does not duplicate.
    if ($(firstColumn).text().length > 0){
      $(firstColumn).html('')
      $(secondColumn).html('')
      $(thirdColumn).html('')
      $(fourthColumn).html('')
      $(fifthColumn).html('')
      $(sixthColumn).html('')
    }
    // The maximum number of lines per column is set to 9.
    data.result.forEach(function(x){
      if(paragraphCounter < 9){
        $(firstColumn).append("<br>" + x + "<br>")
        paragraphCounter += 1
      }
      if (paragraphCounter > 8 && paragraphCounter <= 18){
        paragraphCounter += 1
        $(secondColumn).append("<br>" + x + "<br>")
      }
      if (paragraphCounter > 18 && paragraphCounter <= 27){
        paragraphCounter += 1
        $('#thirdColumn p').append("<br>" + x + "<br>")
      }
      if (paragraphCounter > 27 && paragraphCounter <= 36){
        paragraphCounter += 1
        $('#fourthColumn p').append("<br>" + x + "<br>")
      }
      if (paragraphCounter > 36 && paragraphCounter <= 45){
        paragraphCounter += 1
        $('#fifthColumn p').append("<br>" + x + "<br>")
      }
      if (paragraphCounter > 45 && paragraphCounter <= 54){
        paragraphCounter += 1
        $('#sixthColumn p').append("<br>" + x + "<br>")
      }


    })
  })
}

// Switch between columns 2 to 6.
$('#rightArrow').on('click', switchRight)
$('#leftArrow').on('click', switchLeft)
const columnsArray =[document.querySelector('#secondColumn p'), document.querySelector('#thirdColumn p'), document.querySelector('#fourthColumn p'), document.querySelector('#fifthColumn p'), document.querySelector('#sixthColumn p')]
// The functions swith right or left between columns containing all the gained attributes.
function switchRight(){
  for (x of columnsArray){
    if ($(x).is(':visible')){
      let toggledColumnIndex = columnsArray.indexOf(x)
      let columnToDisplay = columnsArray[toggledColumnIndex + 1]
      if ($(columnToDisplay).text().length > 0){
            $(x).toggle()
            $(columnToDisplay).css('display', 'block')
            break;
          }else{
            $(x).toggle()
            columnToDisplay = columnsArray[0]
            $(columnToDisplay).css('display', 'block')
          }
    }
  }
}

function switchLeft(){
  let endColumnIndex = null
  for(c of columnsArray){
    if (c.textContent.length === 0){
      endColumnIndex = columnsArray.indexOf(c)
      break;
    }
  }
  for (x of columnsArray){
    if ($(x).is(':visible')){
      if (x === columnsArray[0]){
        let toggledColumnIndex = columnsArray.indexOf(x)
        let columnToDisplay = columnsArray[toggledColumnIndex + (endColumnIndex - 1)]
        if ($(columnToDisplay).text().length > 0){
              $(x).toggle()
              $(columnToDisplay).css('display', 'block')
              break;
            }else{
              $(x).toggle()
              columnToDisplay = columnsArray[0]
              $(columnToDisplay).css('display', 'block')
            }
      }else{
        let toggledColumnIndex = columnsArray.indexOf(x)
        let columnToDisplay = columnsArray[toggledColumnIndex - 1]
        if (columnToDisplay.textContent.length > 0){
              $(x).toggle()
              $(columnToDisplay).css('display', 'block')
              break;
            }else{
              $(x).toggle()
              columnToDisplay = columnsArray[0]
              $(columnToDisplay).css('display', 'block')
            }
      }

      
    }
  }
}