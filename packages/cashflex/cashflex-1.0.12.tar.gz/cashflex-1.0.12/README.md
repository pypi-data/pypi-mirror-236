# Cashflex Money Manager
A simple application for managing and forecasting cashflex for individuals and small businesses.

<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/901fc40580bfccc6dbbe6ccaf66c2b21e293a401/icons/128x128/uk.co.contrelec.cashflex.svg" />
</p>

## Overview
Cashflex is a simple application for budgeting and managing domestic finances for Ubuntu. It has a forecasting feature which allows current expenditure and income to be projected into the future so that important decisions about the affordability of major purchases and long-term investments can be made, allowing for inflation and investment growth.
## Basic Principles
Cashflex works on the principle of 'pockets'. Pockets are simply a way of organising chunks of money into convenient blocks. Typically, pockets would be used to represent the following:
- a current account
- a savings account
- a pot for saving for a car
- long term savings
- a pension fund

Each pocket can either be used as it is, or broken out into component. Components are categorised into income or payments. For example, your Current Account pocket might include the following components:

- Income
    - salary
    - pension
    - benefits
  
- Payments
    - mortgage/rent
    - utilities
    - food bill
    - clothing
    - fuel
    - vehicle tax
    - home insurance
  
Each component can be set to repeat regularly. For example, your mortgage might be due every month, whereas other bills such as home insurance might be annual payments.

It is also possible to send payments to other pockets. This feature would be used if you have a regular payment into a savings account.

>Tip: Your budgeting can be as accurate as you need it. One convenient way of avoiding painstaking levels of detail which need constant maintenance is to add up your annual credit card payments, divide by 12, and make this a monthly payment.

Once your pockets and components have been created you can run a forecast to see how your income and expenditure affects your situation into the future.

## Installation
Cashflex is a python application.

There are several ways to install it:

### Method 1: Simple Install

- download the install.sh file from https://github.com/gary-1959/cashflex.
- make the file executable with the command: `chmod +x filename.sh`
- run the installation: `./install.sh` which installs the source files to a sub-folder in your home folder, and adds a shortcut on your desktop. 
- To specify a different folder: `./install.sh <path-to-your-folder>` 

The application will not run without the required dependancies:
  
#### Python 3
Python 3.10 or later is required, together with PyGObject and other dependancies. Install with the following command:

`sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 python3-pip`

#### Matplotlib
Matplotlib 3.8 or later is required. Install with the following command:

`pip install matplotlib`

If all dependencies are satisfied the application will run by double-clicking the desktop icon. Alternatively it can be run the terminal (replace \<installation folder\> with your installation folder):

`cd <installation folder> && python3 cashflex`

On first run, an empty database is created in a hidden .cashflex folder in your home folder ready for you to begin creating pockets and components.

### Method 2: Pip Install

If you don't' have python3 or pip installed, install with:

`sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 python3-pip`

Then enter the following to install cashflex to your home folder. To change the location change the --target directive. Leaving out the --target directive will install it tou your default python folders. Good luck finding it!

`pip install cashflex --target ~/cashflex`

To run the program navigate to your target folder and enter:

`python3 cashflex`

### Method 2: Pip Install in Virtual Environment

Follow the instruction widely available on the internet for creating and activating a python virtual environment and install with:

`pip install cashflex`

Navigate to the python3 installation folder an enter:

`python3 cashflex`

## Creating Pockets
Most installations will require a Current Account or similar, and a Savings Account, so we will create a Current Account with periodic income and payments, and a Savings Account which we will use to accept regular savings amounts.

Start the program, and make sure the POCKETS tab is selected. Click the ADD POCKET icon as shown:
<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/add_pocket.svg" />
</p>

This will create a new pocket in the pockets list:
<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/new_pocket.svg" />
</p>

Fill in the following details:
- NAME:  enter Current Account or a name of your choosing.
- DESCRIPTION: enter a description (optional).
- TYPE: select the type of account this is. This has no operational significance (optional).
- SORT CODE: enter the sort code, for reference purposes
- ACCOUNT NUMBER: enter the account number, for reference purposes
- BALANCE: enter the current balance in the account
- GROWTH: enter the interest rate (APR) on this account

Our Current Account pocket now looks something like this:
<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/pocket_current_account.svg" />
</p>

While we are at it, let's go ahead and create our Savings Account pocket:

<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/pocket_savings_account.svg" />
</p>

Now that we have two pockets created let's go ahead and add some components. The Savings Account is just a repository so nothing more needs to be done here. Select the Current Account row by clicking anywhere on it. Once selected it will be highlighted in green.

Let's add an INCOME source to our Current Account pocket. With Current Account selected click the INCOME tab followed by the ADD INCOME icon.

<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/add_income.svg" />
</p>

This adds a blank INCOME component for you to complete:

<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/add_income_component.svg" />
</p>

Complete as follows:
- ACTIVE: leave ticked. If un-ticked this component will be excluded from forecasts.
- NAME: enter Monthly Salary or a name of your choosing.
- DESCRIPTION: enter a description (optional).
- AMOUNT: enter the amount of your monthly salary
- FREQUENCY: this is paid every month. so enter 1 here, then
- INTERVAL: select MONTH for the interval
- START DATE: enter the date of your next payment in the format YYYY-MM-DD or click the adjacent calendar icon and select a date from the calendar.
- END DATE: select a date some time into the future. You can set a specific date if you know when the payments are going to stop, otherwise just enter a date a long way into the future.
- LAST UPDATE: leave as-is. It is used by the system to know when the last payment was made and would only ever be altered to correct an error, or to skip a payment.
- SEND TO: the default action is to send the payment to the PARENT which is the Pocket which owns this component, But it could equally be sent to another pocket. Leave it as PARENT and on the date specified, every month, the balance of the Current Account pocket will increase by the amount set.
- GROWTH: leave at zero for the moment. This is only used if you know that this income is going to rise (or fall if a negative number is entered) by a percentage every year.

Our component should now look something like this:
<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/income_component_complete.svg" />
</p>

>Tip: You can add as many income sources as you like. If you have two jobs, or involved with contract work, make multiple entries. Use the END DATE if you know when a contract will end.

Now we will add some PAYMENT components, which represent outgoings. Click the PAYMENTS tab, followed by the ADD PAYMENT icon:
<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/add_payment.svg" />
</p>

This adds a blank PAYMENT component for you to complete:
<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/payment_component.svg" />
</p>

Let's add some payments. All payments have the SEND TO column set to PARENT by default (which means the money will be deducted from the parent balance) except one, which is a regular payment into the savings account. In this case the amount is deducted from the Current Account pocket and added to the Savings Account pocket. Our payments components page now looks like this:
<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/payment_components.svg" />
</p>

With all our payments and incomes entered, we are ready to run a forecast!

## Forecasting
Click on the FORECAST tab to switch to the Forecasting page:
<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/forecast_page.svg" />
</p>

Before running a forecast it is a good idea to click the PROCESS TRANSACTIONS button. This ensures that all transactions are up-to-date (this also runs automatically on start-up). The program will tell you if there are any outstanding transactions, and give you the option of processing them now. You have outstanding transactions if you have not opened the program for a while.

Next, we need a timescale for our forecast. If we want to look ahead 5 years we could enter a TIMESCALE of 5 and select YEAR as the interval, but this would give us only 5 data points. A better option would be to select MONTH and enter 60 as the TIMESCALE or, for even more detail, 260 with WEEK selected.

We can enter a number to compensate for inflation by entering a percentage rate (APR) in the INFLATION box. This means that the balances looking ahead will represent spending power in today's money. A reasonable value would be 4%.

Finally, we need to select what we want to see in the forecast by ticking the pockets we would like to see. Select our Current Account and Savings Account pockets.

Click the RUN FORECAST button to see how things will work out in the future:

<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/forecast_1.svg" />
</p>

This puts two lines on the chart: the blue line represents the balance in the Current Account and the orange line shows our Savings Account gradually increasing as each monthly payment goes in.

We can also make an informed judgement that we can reasonably increase our monthly regular savings payment, so switch back to the POCKETS page, select PAYMENTS and adjust the Regular Savings payment to 75. Run the forecast again and we can see that our Current Account stays on a level path and the Savings Account increases more quickly.
<p align="center">
    <img src="https://raw.githubusercontent.com/gary-1959/cashflex/0cac5c6a8ddad51f1554f1de5889d42c4afda744/images/forecast_2.svg" />
</p>

## Additional Features
- All the tables can be re-ordered by clicking and dragging the column header.

- Sorting is possible by clicking on the column header.
- To back up your data simply copy the cashflex.db file located within the .cashflex folder in your home directory, i.e from the command line run the following command:
  
  `cp ~/cashflex/cashflex.db <backup location>`