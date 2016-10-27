*** Settings ***
Library     ../lib/library_rest_helper.py

Suite setup        Setup Suite        ${SERVER ADDRESS}     ${SERVER PORT}     ${INIT LIST}
Suite teardown     Teardown Suite     ${SERVER ADDRESS}     ${SERVER PORT}     ${INIT LIST}

*** Variables ***
${SERVER ADDRESS}         127.0.0.1
${SERVER PORT}            5000
${INIT LIST}              [{"name": "item_0"}, {"name": "item_1"}, {"name": "item_2"}, {"name": "item_3"}, {"name": "item_4"}]
${TEST ITEM 1}            {'name': 'test_item_1', 'serial': '12345', 'email': 'test_1@ssh.com'}
${TEST ITEM 2}            {'name': 'test_item_2', 'serial': '67890', 'email': 'test_2@ssh.com'}
${TEST ITEM WO NAME}      {'email': 'test@ssh.com', 'phone': '0401234567'}

*** Test Cases ***
Test Create and Delete Item
    Create Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ${TEST ITEM 1}
    Verify Item Exist In List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ${TEST ITEM 1}
    Delete Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ${TEST ITEM 1}
    Verify Item Not Exist In List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ${TEST ITEM 1}

Test Get Item Exist In List
    [Setup]     Setup Test Create And Verify     ${SERVER ADDRESS}     ${SERVER PORT}     ${TEST ITEM 1}
    Get Item Exist In List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ${TEST ITEM 1}
    [Teardown]     Teardown Test Delete And Verify     ${SERVER ADDRESS}     ${SERVER PORT}     ${TEST ITEM 1}

Test Get Item Not Exist In List
    Get Item Not Exist In List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ${TEST ITEM 2}

Test Delete Non Existing Item
    Delete Non Existing Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ${TEST ITEM 2}

Test Create Duplicated Item
    [Setup]     Setup Test Create And Verify     ${SERVER ADDRESS}     ${SERVER PORT}     ${TEST ITEM 1}
    Create Duplicate Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ${TEST ITEM 1}
    [Teardown]     Teardown Test Delete And Verify     ${SERVER ADDRESS}     ${SERVER PORT}     ${TEST ITEM 1}

Test Create Item Without Name
    Create Item Without Name
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ${TEST ITEM WO NAME}

*** Keywords ***
Setup Suite
    [Arguments]                  ${SERVER ADDRESS}     ${SERVER PORT}     ${ITEM}
    Verify Server Is Running     ${SERVER ADDRESS}     ${SERVER PORT}
    Verify Initialized List      ${SERVER ADDRESS}     ${SERVER PORT}     ${ITEM}

Setup Test Create And Verify
    [Arguments]                   ${SERVER ADDRESS}     ${SERVER PORT}     ${ITEM}
    Create Item                   ${SERVER ADDRESS}     ${SERVER PORT}     ${ITEM}
    Verify Item Exist In List     ${SERVER ADDRESS}     ${SERVER PORT}     ${ITEM}

Teardown Test Delete And Verify
    [Arguments]                        ${SERVER ADDRESS}     ${SERVER PORT}     ${ITEM}
    Delete Item                        ${SERVER ADDRESS}     ${SERVER PORT}     ${ITEM}
    Verify Item Not Exist In List      ${SERVER ADDRESS}     ${SERVER PORT}     ${ITEM}
