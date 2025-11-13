db = db.getSiblingDB('financials');
db.createCollection('expenses');

db.expenses.insertMany([
    { date: new Date("2024-01-01"), category: "Office", amount: 45.90 },
    { date: new Date("2024-01-02"), category: "Travel", amount: 120.00 },
    { date: new Date("2024-01-03"), category: "Meals", amount: 18.50 },
    { date: new Date("2024-01-04"), category: "Software", amount: 29.99 },
    { date: new Date("2024-01-05"), category: "Office", amount: 67.20 },
    { date: new Date("2024-01-06"), category: "Marketing", amount: 200.00 },
    { date: new Date("2024-01-07"), category: "Travel", amount: 89.00 },
    { date: new Date("2024-01-08"), category: "Meals", amount: 22.10 },
    { date: new Date("2024-01-09"), category: "Software", amount: 14.00 },
    { date: new Date("2024-01-10"), category: "Office", amount: 34.50 },
    { date: new Date("2024-01-11"), category: "Travel", amount: 155.40 },
    { date: new Date("2024-01-12"), category: "Meals", amount: 16.00 },
    { date: new Date("2024-01-13"), category: "Marketing", amount: 120.00 },
    { date: new Date("2024-01-14"), category: "Office", amount: 53.70 },
    { date: new Date("2024-01-15"), category: "Software", amount: 39.99 },
    { date: new Date("2024-01-16"), category: "Travel", amount: 210.00 },
    { date: new Date("2024-01-17"), category: "Meals", amount: 12.80 },
    { date: new Date("2024-01-18"), category: "Office", amount: 27.90 },
    { date: new Date("2024-01-19"), category: "Travel", amount: 98.00 },
    { date: new Date("2024-01-20"), category: "Marketing", amount: 300.00 }
]);

print("Dummy expenses inserted.");