# Symptom-Aware Nutrition Engine
# Evidence-informed symptom to nutrient mapping for cycle-aligned nutrition

# Ingredient descriptions for hover tooltips
INGREDIENT_BENEFITS = {
    "pumpkin seeds": "Rich in magnesium which helps reduce muscle tension and inflammation",
    "almonds": "Packed with magnesium and vitamin E to ease cramps and support mood",
    "spinach": "Iron-rich leafy green that boosts energy and supports oxygen transport",
    "dark chocolate": "Contains magnesium and phenylethylamine to ease cramps and lift mood",
    "avocado": "Potassium-rich and full of healthy fats for hormone balance",
    "walnuts": "Omega-3 powerhouse that supports brain health and reduces inflammation",
    "flaxseed": "Omega-3s and lignans to support hormone balance and reduce inflammation",
    "chia seeds": "High in omega-3s and fiber to support digestion and mood",
    "dried cranberries": "Antioxidant-rich to support immune health during menstruation",
    "almond milk": "Gentle on digestion and fortified with calcium for bone health",
    "maple syrup": "Natural sweetener with minerals that support energy levels",
    "berries": "Antioxidant powerhouses that reduce inflammation and support mood",
    "coconut": "Medium-chain fats for sustained energy and hormone support",
    "lentils": "Plant-based protein and iron to combat fatigue naturally",
    "chickpeas": "Complete protein with fiber to stabilize blood sugar and energy",
    "red meat": "Heme iron (most bioavailable form) to replenish blood loss during menstruation",
    "fortified cereals": "B vitamins to convert food into energy efficiently",
    "eggs": "Complete protein and choline to support brain health and mood",
    "salmon": "Omega-3 rich fatty fish for mood support and inflammation reduction",
    "beef": "Bioavailable iron and B vitamins for sustained energy",
    "tofu": "Plant-based protein for sustained energy and hormone balance",
    "quinoa": "Complete protein with all amino acids for energy and recovery",
    "carrots": "Beta-carotene for immunity and overall wellness",
    "celery": "Hydrating and contains potassium to reduce bloating",
    "tomato": "Lycopene antioxidant to reduce inflammation and support heart health",
    "garlic": "Immune-boosting and antimicrobial compounds",
    "vegetable broth": "Hydrating mineral source for electrolyte balance",
    "roasted chickpeas": "Protein-rich snack for sustained energy",
    "sweet potato": "Complex carbs and beta-carotene for sustained energy and hormone support",
    "tahini": "Calcium and magnesium for bone health and muscle relaxation",
    "lemon": "Vitamin C to enhance iron absorption and support immunity",
    "ginger": "Anti-inflammatory and aids digestion to reduce bloating",
    "fennel tea": "Soothes digestive system and naturally reduces bloating",
    "leafy greens": "Iron, folate, and magnesium for energy and cycle support",
    "cucumber": "Hydrating with potassium to reduce water retention",
    "coconut water": "Natural electrolytes to rehydrate and reduce bloating",
    "bone broth": "Collagen and minerals to support gut health and digestion",
    "papaya": "Digestive enzymes and potassium to ease bloating",
    "kimchi": "Probiotics for gut health and immune support",
    "pineapple": "Bromelain enzyme aids digestion and reduces bloating",
    "coconut milk": "Medium-chain fats for sustained energy and satiety",
    "ice": "Hydration and satisfying texture",
    "fresh ginger": "Anti-inflammatory to soothe the digestive system",
    "fennel seeds": "Naturally reduces gas and bloating",
    "hot water": "Aids digestion and helps relax the digestive system",
    "honey": "Natural glucose for quick energy and antioxidants",
    "dates": "Natural sugars and magnesium for energy and cramp relief",
    "cocoa powder": "Magnesium and mood-boosting phenylethylamine",
    "shredded coconut": "Healthy fats and fiber for sustained energy",
    "almond butter": "Protein and healthy fats for sustained energy and satiety",
    "banana": "Potassium and glucose for quick energy and mood support",
    "cinnamon": "Helps regulate blood sugar and adds warmth",
    "fatty fish": "Omega-3s for brain health and inflammation reduction",
    "turkey": "Tryptophan amino acid precursor to serotonin",
    "chicken": "Lean protein and B vitamins for sustained energy",
    "cheese": "Calcium, protein, and tryptophan for mood support",
    "whole grains": "B vitamins and fiber for sustained energy and blood sugar stability",
    "dark chocolate chips": "Magnesium and mood-boosting compounds",
    "brown rice": "B vitamins and fiber for sustained energy",
    "broccoli": "Vitamin C and calcium for bone health and immunity",
    "olive oil": "Anti-inflammatory monounsaturated fats",
    "oats": "Beta-glucans for sustained energy and heart health",
    "Greek yogurt": "Protein and probiotics for energy and gut health",
    "granola": "Complex carbs and crunchy satisfaction for energy",
    "sea salt": "Minerals and sodium for electrolyte balance",
    "apple": "Fiber and glucose for sustained energy and blood sugar stability"
}

SYMPTOM_NUTRIENT_MAP = {
    "cramps": {
        "nutrients": ["magnesium", "calcium", "omega-3"],
        "reasoning": "Magnesium and calcium help relax muscles and reduce inflammation. Omega-3s support hormone balance.",
        "foods": [
            "pumpkin seeds", "almonds", "spinach", "dark chocolate (70%+)",
            "avocado", "walnuts", "flaxseed", "chia seeds"
        ],
        "recipes": [
            {
                "name": "Magnesium-Rich Trail Mix",
                "ingredients": ["pumpkin seeds", "almonds", "dark chocolate chips", "dried cranberries"],
                "time": "5 mins",
                "instructions": "Mix equal parts seeds, almonds, and dark chocolate. Add cranberries. Enjoy!"
            },
            {
                "name": "Omega-3 Chia Pudding",
                "ingredients": ["chia seeds", "almond milk", "maple syrup", "berries", "coconut"],
                "time": "overnight",
                "instructions": "Mix 1/3 cup chia seeds with 1 cup almond milk. Add 1 tbsp maple syrup. Let sit overnight. Top with berries and coconut."
            }
        ]
    },
    "fatigue": {
        "nutrients": ["iron", "B vitamins", "protein", "carbs"],
        "reasoning": "Iron carries oxygen in your blood. B vitamins help convert food to energy. Balanced macros sustain energy.",
        "foods": [
            "lentils", "chickpeas", "spinach", "red meat", "fortified cereals",
            "eggs", "salmon", "beef", "tofu", "pumpkin seeds", "quinoa"
        ],
        "recipes": [
            {
                "name": "Iron-Boosting Lentil Soup",
                "ingredients": ["lentils", "spinach", "carrots", "celery", "tomato", "garlic", "vegetable broth"],
                "time": "30 mins",
                "instructions": "Sauté garlic, carrots, celery. Add lentils and broth. Simmer 20 mins. Add spinach and tomato. Cook 5 more mins."
            },
            {
                "name": "Energy Bowl",
                "ingredients": ["quinoa", "roasted chickpeas", "sweet potato", "spinach", "tahini", "lemon"],
                "time": "25 mins",
                "instructions": "Cook quinoa. Roast chickpeas with cumin. Roast sweet potato. Assemble bowl. Drizzle with tahini-lemon dressing."
            }
        ]
    },
    "bloating": {
        "nutrients": ["fiber", "potassium", "anti-inflammatory foods"],
        "reasoning": "Gentle fiber aids digestion. Potassium reduces water retention. Anti-inflammatory foods soothe the gut.",
        "foods": [
            "ginger", "fennel tea", "leafy greens", "berries", "cucumber",
            "coconut water", "bone broth", "sweet potato", "papaya", "kimchi"
        ],
        "recipes": [
            {
                "name": "Bloat-Busting Green Smoothie",
                "ingredients": ["spinach", "ginger", "cucumber", "pineapple", "coconut milk", "ice"],
                "time": "5 mins",
                "instructions": "Blend spinach, 1 inch ginger, cucumber, pineapple, 1 cup coconut milk, and ice until smooth."
            },
            {
                "name": "Ginger-Fennel Tea",
                "ingredients": ["fresh ginger", "fennel seeds", "hot water", "honey", "lemon"],
                "time": "10 mins",
                "instructions": "Steep 1 tbsp sliced ginger and 1 tsp fennel seeds in hot water for 10 mins. Strain. Add honey and lemon."
            }
        ]
    },
    "cravings": {
        "nutrients": ["magnesium", "glucose", "fat"],
        "reasoning": "Cravings often signal nutrient needs. Chocolate cravings suggest magnesium. Sweet cravings suggest energy/glucose needs.",
        "foods": [
            "dark chocolate", "nuts", "dried fruit", "honey", "sweet potato",
            "banana", "whole grain bread", "almond butter", "dates", "trail mix"
        ],
        "recipes": [
            {
                "name": "Healthy Chocolate Energy Bites",
                "ingredients": ["almond butter", "dates", "cocoa powder", "shredded coconut"],
                "time": "15 mins",
                "instructions": "Process dates, almond butter, cocoa, and coconut. Roll into balls. Refrigerate."
            },
            {
                "name": "Sweet Potato Toast",
                "ingredients": ["sweet potato", "almond butter", "banana", "honey", "cinnamon"],
                "time": "10 mins",
                "instructions": "Toast sweet potato slices. Spread with almond butter. Top with banana slices, drizzle honey, sprinkle cinnamon."
            }
        ]
    },
    "mood dips": {
        "nutrients": ["omega-3", "B vitamins", "serotonin precursors"],
        "reasoning": "Omega-3s support brain health. B vitamins help regulate mood. Tryptophan supports serotonin production.",
        "foods": [
            "fatty fish", "walnuts", "flaxseed", "eggs", "chickpeas",
            "turkey", "chicken", "cheese", "whole grains", "berries", "dark chocolate"
        ],
        "recipes": [
            {
                "name": "Brain-Boosting Buddha Bowl",
                "ingredients": ["brown rice", "salmon", "avocado", "broccoli", "walnuts", "olive oil"],
                "time": "30 mins",
                "instructions": "Cook rice. Pan-sear salmon. Roast broccoli. Assemble. Drizzle with olive oil. Top with walnuts."
            },
            {
                "name": "Mood-Lifting Smoothie",
                "ingredients": ["banana", "almond butter", "oats", "honey", "dark chocolate", "almond milk"],
                "time": "5 mins",
                "instructions": "Blend banana, 2 tbsp almond butter, 1/2 cup oats, 1 tbsp honey, 1 tbsp cocoa powder, 1 cup almond milk."
            }
        ]
    },
    "low energy": {
        "nutrients": ["glucose", "B vitamins", "protein", "iron"],
        "reasoning": "Quick energy from healthy carbs. B vitamins convert food to ATP. Protein stabilizes blood sugar.",
        "foods": [
            "oats", "brown rice", "whole grain bread", "banana", "apple",
            "nuts", "seeds", "eggs", "Greek yogurt", "granola", "dark chocolate"
        ],
        "recipes": [
            {
                "name": "Sustained Energy Oatmeal",
                "ingredients": ["oats", "almond milk", "banana", "almond butter", "honey", "cinnamon"],
                "time": "10 mins",
                "instructions": "Cook oats in almond milk. Top with sliced banana, almond butter, honey drizzle, and cinnamon."
            },
            {
                "name": "Protein Power Balls",
                "ingredients": ["oats", "almond butter", "honey", "dark chocolate chips", "sea salt"],
                "time": "15 mins",
                "instructions": "Mix 1 cup oats, 1/2 cup almond butter, 1/4 cup honey. Roll into balls. Dip in melted chocolate. Chill."
            }
        ]
    }
}

CYCLE_PHASE_NUTRITION = {
    "menstruation": {
        "focus": "Replenish and nourish",
        "key_nutrients": ["iron", "B vitamins", "magnesium"],
        "suggested_foods": ["red meat", "spinach", "lentils", "dark chocolate", "ginger tea"],
        "tip": "Your body needs more calories this week. Honor your appetite and prioritize nutrient-dense foods."
    },
    "follicular": {
        "focus": "Build energy and optimism",
        "key_nutrients": ["B vitamins", "protein", "antioxidants"],
        "suggested_foods": ["berries", "citrus", "leafy greens", "lean proteins", "whole grains"],
        "tip": "Rising estrogen means you can tolerate more intense workouts. Eat lighter, brighter foods."
    },
    "ovulation": {
        "focus": "Stabilize mood and hormones",
        "key_nutrients": ["omega-3", "serotonin precursors", "antioxidants"],
        "suggested_foods": ["fatty fish", "walnuts", "dark chocolate", "berries", "avocado"],
        "tip": "You're at peak energy! Metabolism is highest now. Enjoy satisfying, nourishing meals."
    },
    "luteal": {
        "focus": "Soothe and sustain",
        "key_nutrients": ["magnesium", "calcium", "complex carbs", "iron"],
        "suggested_foods": ["sweet potato", "chickpeas", "almonds", "whole grains", "leafy greens"],
        "tip": "Your body needs more calories and carbs now. Embrace comforting, warm foods."
    }
}

FOOD_BENEFITS = {
    "pumpkin seeds": "Rich in magnesium and zinc - helps ease muscle tension and supports immune health",
    "almonds": "High in magnesium and protein - soothes cramping and provides sustained energy",
    "spinach": "Iron powerhouse - replenishes oxygen in your blood and boosts energy levels",
    "dark chocolate": "Contains magnesium and serotonin boosters - lifts mood naturally",
    "avocado": "Full of potassium and healthy fats - reduces water retention and supports hormone balance",
    "walnuts": "Omega-3 rich - calms inflammation and supports mood and brain health",
    "flaxseed": "Plant-based omega-3s - helps regulate hormones and reduces inflammation",
    "chia seeds": "Fiber and omega-3 combo - soothes digestion and supports steady energy",
    "lentils": "Iron and protein packed - perfect for fatigue and building strength",
    "chickpeas": "Complete protein with fiber - stabilizes blood sugar and reduces bloating",
    "red meat": "High-quality iron - directly addresses fatigue during menstruation",
    "fortified cereals": "B vitamins galore - converts food into energy your body needs",
    "eggs": "Complete protein with choline - supports brain function and mood stability",
    "salmon": "Omega-3 and vitamin D - anti-inflammatory powerhouse for mood and joint health",
    "beef": "Highly absorbable iron - the most effective way to combat fatigue",
    "tofu": "Plant-based iron and protein - excellent for vegetarians managing fatigue",
    "quinoa": "Complete protein with fiber - sustained energy without crashes",
    "ginger": "Anti-inflammatory and digestive aid - soothes cramping and bloating",
    "fennel tea": "Gentle digestive support - reduces bloating and cramping naturally",
    "leafy greens": "Mineral dense - replenishes magnesium and calcium for muscle relaxation",
    "berries": "Antioxidant rich - reduces inflammation and stabilizes mood",
    "cucumber": "Hydrating and potassium-rich - reduces water retention and bloating",
    "coconut water": "Electrolyte rich - rehydrates and reduces bloating from mineral loss",
    "bone broth": "Collagen and minerals - heals gut lining and reduces inflammation",
    "sweet potato": "Complex carbs and beta-carotene - sustained energy and hormone support",
    "papaya": "Enzyme and vitamin C - aids digestion and reduces bloating",
    "kimchi": "Probiotics and spice - supports gut health and reduces bloating",
    "pineapple": "Bromelain enzyme - natural anti-inflammatory for digestion",
    "honey": "Natural glucose - quick energy boost with mineral content",
    "dates": "Natural magnesium and glucose - perfect craving satisfier",
    "almond butter": "Magnesium and protein - satisfies cravings and provides lasting energy",
    "banana": "Potassium and B vitamins - reduces water retention and provides quick energy",
    "whole grain bread": "B vitamins and fiber - steady energy without blood sugar crashes",
    "trail mix": "Balanced nutrients - sustained energy with natural sugars and healthy fats",
    "Greek yogurt": "Probiotics and protein - supports gut health and mood",
    "granola": "Complex carbs and fiber - sustained energy throughout the day",
    "brown rice": "B vitamins and fiber - slow-release energy for endurance",
    "oats": "Beta-glucan and B vitamins - steady energy and mood support",
    "apple": "Fiber and antioxidants - stabilizes energy and supports digestion",
    "cheese": "Calcium and protein - supports muscle function and mood",
    "seeds": "Comprehensive minerals - magnesium, zinc, and iron together",
    "nuts": "Healthy fats and magnesium - reduces inflammation and supports hormones",
    "tuna": "Omega-3 and selenium - brain and mood support",
    "turkey": "Tryptophan rich - supports serotonin production and mood",
    "chicken": "Lean protein and B vitamins - sustains energy without heaviness",
    "fatty fish": "Omega-3 powerhouse - fights inflammation and supports mental health",
    "whole grains": "B vitamins and fiber - converts nutrients into sustained energy"
}

# Menopausal phase symptoms and nutrient mapping
MENOPAUSAL_SYMPTOMS = {
    "hot flashes": {
        "nutrients": ["phytoestrogens", "vitamin E", "magnesium"],
        "reasoning": "Phytoestrogens from plant sources help regulate body temperature. Magnesium supports nervous system calm. Vitamin E aids hormonal transitions.",
        "foods": [
            "soy products", "flaxseed", "lentils", "chickpeas", "sesame seeds",
            "almonds", "spinach", "sweet potato", "whole grains", "berries"
        ],
        "recipes": [
            {
                "name": "Cooling Miso Soup with Tofu",
                "ingredients": ["silken tofu", "miso paste", "vegetable broth", "spinach", "green onions", "ginger"],
                "time": "15 mins",
                "instructions": "Heat broth gently. Dissolve miso paste. Add cubed tofu, spinach, and ginger. Simmer 5 mins. Top with green onions."
            },
            {
                "name": "Phytoestrogen Smoothie Bowl",
                "ingredients": ["unsweetened soy milk", "flaxseed", "berries", "granola", "coconut", "honey"],
                "time": "5 mins",
                "instructions": "Blend soy milk with 1 tbsp ground flaxseed. Pour into bowl. Top with berries, granola, and coconut flakes."
            }
        ]
    },
    "night sweats": {
        "nutrients": ["phytoestrogens", "calcium", "iron", "B vitamins"],
        "reasoning": "Phytoestrogens stabilize temperature fluctuations. Calcium supports bone health during hormonal shifts. Iron replenishes losses from night sweats.",
        "foods": [
            "soy", "tempeh", "edamame", "red clover", "sage", "calcium-fortified foods",
            "spinach", "sesame seeds", "salmon", "eggs", "whole grains"
        ],
        "recipes": [
            {
                "name": "Cooling Green Tea with Sage",
                "ingredients": ["green tea", "fresh sage", "honey", "lemon", "ice"],
                "time": "10 mins",
                "instructions": "Brew green tea with fresh sage leaves. Cool. Add honey, lemon juice, and ice. Sip throughout evening."
            },
            {
                "name": "Calcium-Rich Buddha Bowl",
                "ingredients": ["tempeh", "spinach", "sesame seeds", "sweet potato", "tahini", "olive oil"],
                "time": "25 mins",
                "instructions": "Marinate and bake tempeh. Roast sweet potato. Assemble over spinach. Drizzle tahini dressing. Sprinkle sesame seeds."
            }
        ]
    },
    "brain fog": {
        "nutrients": ["omega-3", "B vitamins", "antioxidants", "iron"],
        "reasoning": "Omega-3s support cognitive function and memory. B vitamins aid energy production for focus. Antioxidants protect brain cells. Iron carries oxygen to the brain.",
        "foods": [
            "fatty fish", "walnuts", "flaxseed", "chia seeds", "blueberries",
            "spinach", "eggs", "whole grains", "dark chocolate", "turmeric"
        ],
        "recipes": [
            {
                "name": "Brain-Boosting Oatmeal",
                "ingredients": ["rolled oats", "almond milk", "walnuts", "blueberries", "honey", "cinnamon"],
                "time": "10 mins",
                "instructions": "Cook oats in almond milk. Top with chopped walnuts, fresh blueberries, honey drizzle, and cinnamon."
            },
            {
                "name": "Golden Milk Latte",
                "ingredients": ["turmeric", "ginger", "cinnamon", "almond milk", "honey", "black pepper"],
                "time": "5 mins",
                "instructions": "Warm almond milk. Whisk in 1 tsp turmeric, 1/2 tsp ginger, pinch of black pepper. Add honey. Sprinkle cinnamon."
            }
        ]
    },
    "sleep disruption": {
        "nutrients": ["magnesium", "tryptophan", "melatonin precursors", "B vitamins"],
        "reasoning": "Magnesium promotes relaxation and better sleep quality. Tryptophan supports serotonin and melatonin production. B vitamins regulate sleep cycles.",
        "foods": [
            "almonds", "pumpkin seeds", "tart cherry juice", "turkey", "chicken",
            "chickpeas", "spinach", "sweet potato", "whole grains", "chamomile"
        ],
        "recipes": [
            {
                "name": "Sleepy Tart Cherry Smoothie",
                "ingredients": ["tart cherry juice", "almond milk", "banana", "almonds", "honey"],
                "time": "5 mins",
                "instructions": "Blend tart cherry juice, almond milk, banana, and 1/4 cup almonds. Add honey. Drink 1 hour before bed."
            },
            {
                "name": "Calming Herb Tea Blend",
                "ingredients": ["chamomile", "lavender", "valerian root", "honey", "almond milk"],
                "time": "10 mins",
                "instructions": "Steep 1 tsp each of chamomile and lavender in hot water. Strain. Add honey and warm almond milk."
            }
        ]
    },
    "joint stiffness": {
        "nutrients": ["omega-3", "collagen", "vitamin D", "calcium"],
        "reasoning": "Omega-3s reduce joint inflammation. Collagen supports joint structure. Vitamin D and calcium maintain bone and cartilage health during hormonal transitions.",
        "foods": [
            "fatty fish", "bone broth", "walnuts", "chia seeds", "leafy greens",
            "almonds", "sesame seeds", "citrus", "eggs", "mushrooms"
        ],
        "recipes": [
            {
                "name": "Anti-Inflammatory Turmeric Rice",
                "ingredients": ["brown rice", "turmeric", "ginger", "coconut milk", "spinach", "almonds"],
                "time": "30 mins",
                "instructions": "Cook brown rice with turmeric and ginger. Stir in spinach and coconut milk. Top with sliced almonds."
            },
            {
                "name": "Bone Broth and Vegetable Soup",
                "ingredients": ["bone broth", "spinach", "carrots", "celery", "ginger", "turmeric"],
                "time": "20 mins",
                "instructions": "Heat bone broth. Add ginger, turmeric, carrots, celery. Simmer 10 mins. Add fresh spinach. Season to taste."
            }
        ]
    },
    "mood variability": {
        "nutrients": ["serotonin precursors", "omega-3", "B vitamins", "magnesium"],
        "reasoning": "Tryptophan supports serotonin production. Omega-3s support mood regulation. B vitamins aid neurotransmitter synthesis. Magnesium reduces anxiety.",
        "foods": [
            "fatty fish", "walnuts", "turkey", "chicken", "eggs", "dark chocolate",
            "berries", "bananas", "leafy greens", "almonds", "whole grains"
        ],
        "recipes": [
            {
                "name": "Mood-Lifting Buddha Bowl",
                "ingredients": ["quinoa", "roasted chickpeas", "spinach", "avocado", "walnuts", "tahini"],
                "time": "25 mins",
                "instructions": "Cook quinoa. Roast chickpeas with paprika. Assemble over spinach with avocado. Drizzle tahini dressing."
            },
            {
                "name": "Chocolate Chia Pudding",
                "ingredients": ["chia seeds", "almond milk", "cocoa powder", "maple syrup", "berries"],
                "time": "overnight",
                "instructions": "Mix 1/3 cup chia, 1 cup almond milk, 2 tbsp cocoa powder, 1 tbsp maple syrup. Chill overnight. Top with berries."
            }
        ]
    },
    "metabolic changes": {
        "nutrients": ["protein", "fiber", "B vitamins", "iron"],
        "reasoning": "Protein maintains muscle mass and metabolic rate during hormonal shifts. Fiber stabilizes blood sugar. B vitamins support energy production. Iron maintains oxygen transport.",
        "foods": [
            "lean meats", "fish", "eggs", "legumes", "nuts", "seeds",
            "whole grains", "leafy greens", "avocado", "berries", "yogurt"
        ],
        "recipes": [
            {
                "name": "High-Protein Breakfast Bowl",
                "ingredients": ["Greek yogurt", "granola", "berries", "nuts", "honey", "flaxseed"],
                "time": "5 mins",
                "instructions": "Layer Greek yogurt in bowl. Top with granola, berries, nuts, honey drizzle, and 1 tbsp ground flaxseed."
            },
            {
                "name": "Protein-Rich Lentil Salad",
                "ingredients": ["lentils", "cherry tomatoes", "cucumber", "feta", "spinach", "lemon", "olive oil"],
                "time": "30 mins",
                "instructions": "Cook lentils. Toss with diced tomatoes, cucumber, spinach, feta. Dress with lemon juice and olive oil."
            }
        ]
    }
}

# Menopausal life phase nutrition guidance
MENOPAUSAL_PHASE_NUTRITION = {
    "perimenopause": {
        "focus": "Navigate hormonal fluctuations with nourishment",
        "key_nutrients": ["phytoestrogens", "omega-3", "magnesium", "B vitamins"],
        "suggested_foods": ["soy products", "fatty fish", "flaxseed", "almonds", "leafy greens", "berries", "whole grains"],
        "tip": "Your hormones are shifting - this is a natural transition, not a flaw. Nourish yourself with phytoestrogen-rich foods and anti-inflammatory choices. Regular, balanced meals help stabilize mood and energy."
    },
    "menopause": {
        "focus": "Support your evolving body with intention",
        "key_nutrients": ["calcium", "vitamin D", "phytoestrogens", "omega-3", "protein"],
        "suggested_foods": ["fortified dairy", "fatty fish", "soy", "sesame seeds", "leafy greens", "eggs", "nuts"],
        "tip": "Your body deserves extra care and nourishment now. Bone health, heart health, and metabolic support are priorities. This phase is an opportunity to honor what your body can do - celebrate your strength and resilience."
    },
    "post-menopause": {
        "focus": "Sustain health, vitality, and strength",
        "key_nutrients": ["calcium", "vitamin D", "protein", "iron", "antioxidants"],
        "suggested_foods": ["fortified foods", "lean proteins", "fatty fish", "leafy greens", "berries", "nuts", "whole grains"],
        "tip": "You've navigated a major transition. Now focus on bone density, heart health, and sustained energy. Your body is wise and strong - nourish it with foods that support long-term vitality."
    }
}


class SymptomNutritionEngine:
    def __init__(self):
        self.symptom_map = SYMPTOM_NUTRIENT_MAP
        self.cycle_phases = CYCLE_PHASE_NUTRITION
        self.menopausal_symptoms = MENOPAUSAL_SYMPTOMS
        self.menopausal_phases = MENOPAUSAL_PHASE_NUTRITION
        self.food_benefits = FOOD_BENEFITS

    def get_symptoms(self, life_phase=None):
        """Return available symptoms based on life phase"""
        if life_phase and life_phase.lower() in ["perimenopause", "menopause", "post-menopause"]:
            return list(self.menopausal_symptoms.keys())
        return list(self.symptom_map.keys())

    def log_symptom(self, symptom, life_phase=None):
        """Get nutrition recommendations for a logged symptom"""
        symptom_lower = symptom.lower()
        
        # Check menopausal symptoms if life phase is specified
        if life_phase and life_phase.lower() in ["perimenopause", "menopause", "post-menopause"]:
            if symptom_lower not in self.menopausal_symptoms:
                return None
            symptom_data = self.menopausal_symptoms[symptom_lower]
        else:
            if symptom_lower not in self.symptom_map:
                return None
            symptom_data = self.symptom_map[symptom_lower]

        return {
            "symptom": symptom_lower,
            "nutrients": symptom_data["nutrients"],
            "reasoning": symptom_data["reasoning"],
            "foods": symptom_data["foods"],
            "recipes": symptom_data["recipes"]
        }

    def get_recommendations(self, symptoms_list, cycle_phase=None, life_phase=None):
        """Generate personalized recommendations based on symptoms and phase (menstrual or menopausal)"""
        all_nutrients = set()
        all_foods = set()
        all_recipes = []
        reasoning_list = []

        # Collect recommendations from each symptom
        for symptom in symptoms_list:
            symptom_data = self.log_symptom(symptom, life_phase)
            if symptom_data:
                all_nutrients.update(symptom_data["nutrients"])
                all_foods.update(symptom_data["foods"])
                all_recipes.extend(symptom_data["recipes"])
                reasoning_list.append({
                    "symptom": symptom,
                    "reason": symptom_data["reasoning"]
                })

        # Add phase-specific recommendations based on life phase
        phase_recommendation = None
        
        if life_phase and life_phase.lower() in self.menopausal_phases:
            # Menopausal phase recommendations
            phase_data = self.menopausal_phases[life_phase.lower()]
            all_nutrients.update(phase_data["key_nutrients"])
            all_foods.update(phase_data["suggested_foods"])
            phase_recommendation = {
                "phase": life_phase,
                "focus": phase_data["focus"],
                "tip": phase_data["tip"]
            }
        elif cycle_phase and cycle_phase.lower() in self.cycle_phases:
            # Menstrual cycle phase recommendations
            phase_data = self.cycle_phases[cycle_phase.lower()]
            all_nutrients.update(phase_data["key_nutrients"])
            all_foods.update(phase_data["suggested_foods"])
            phase_recommendation = {
                "phase": cycle_phase,
                "focus": phase_data["focus"],
                "tip": phase_data["tip"]
            }

        # Deduplicate recipes and limit to top 4
        unique_recipes = {r["name"]: r for r in all_recipes}
        top_recipes = list(unique_recipes.values())[:4]

        return {
            "symptoms": symptoms_list,
            "cycle_phase": cycle_phase,
            "life_phase": life_phase,
            "nutrients": list(all_nutrients),
            "symptom_reasoning": reasoning_list,
            "recommended_foods": list(all_foods),
            "food_benefits": {food: self.food_benefits.get(food, "") for food in all_foods},
            "recipes": top_recipes,
            "phase_insight": phase_recommendation,
            "encouragement": get_encouragement_message(symptoms_list, cycle_phase, life_phase)
        }

    def get_quick_snacks(self, symptoms_list):
        """Get quick 5-minute snack ideas for common symptoms"""
        quick_snacks = {
            "cramps": [
                {"name": "Dark Chocolate + Almonds", "time": "2 mins", "nutrients": "Magnesium, Calcium"},
                {"name": "Banana with Almond Butter", "time": "1 min", "nutrients": "Potassium, Magnesium"}
            ],
            "fatigue": [
                {"name": "Apple with Cheese", "time": "2 mins", "nutrients": "Iron, Protein, Glucose"},
                {"name": "Trail Mix", "time": "1 min", "nutrients": "B Vitamins, Protein"}
            ],
            "bloating": [
                {"name": "Ginger Tea", "time": "5 mins", "nutrients": "Anti-inflammatory"},
                {"name": "Cucumber Slices", "time": "1 min", "nutrients": "Hydration, Potassium"}
            ],
            "cravings": [
                {"name": "Dates Stuffed with Almond Butter", "time": "2 mins", "nutrients": "Magnesium, Energy"},
                {"name": "Sweet Potato Chips", "time": "3 mins", "nutrients": "Complex Carbs"}
            ],
            "mood dips": [
                {"name": "Dark Chocolate + Walnuts", "time": "2 mins", "nutrients": "Omega-3, Serotonin Precursors"},
                {"name": "Yogurt with Berries", "time": "2 mins", "nutrients": "Probiotics, Antioxidants"}
            ],
            "low energy": [
                {"name": "Banana with Granola", "time": "1 min", "nutrients": "Glucose, B Vitamins"},
                {"name": "Peanut Butter Toast", "time": "3 mins", "nutrients": "Protein, Carbs"}
            ],
            # Menopausal symptom snacks
            "hot flashes": [
                {"name": "Chilled Edamame", "time": "2 mins", "nutrients": "Phytoestrogens, Protein"},
                {"name": "Frozen Grapes", "time": "1 min", "nutrients": "Cooling, Antioxidants"},
                {"name": "Iced Green Tea with Mint", "time": "3 mins", "nutrients": "Phytoestrogens, Cooling"}
            ],
            "night sweats": [
                {"name": "Soy Yogurt with Flaxseed", "time": "2 mins", "nutrients": "Phytoestrogens, Omega-3"},
                {"name": "Cool Cucumber Water", "time": "2 mins", "nutrients": "Hydration, Cooling"},
                {"name": "Sesame Crackers", "time": "1 min", "nutrients": "Calcium, Phytoestrogens"}
            ],
            "brain fog": [
                {"name": "Walnuts + Blueberries", "time": "1 min", "nutrients": "Omega-3, Antioxidants"},
                {"name": "Smoked Salmon on Crackers", "time": "3 mins", "nutrients": "Omega-3, B Vitamins"},
                {"name": "Dark Chocolate Square", "time": "1 min", "nutrients": "Flavonoids, Focus"}
            ],
            "sleep disruption": [
                {"name": "Tart Cherry Juice", "time": "1 min", "nutrients": "Melatonin Precursors"},
                {"name": "Warm Almond Milk with Honey", "time": "3 mins", "nutrients": "Tryptophan, Magnesium"},
                {"name": "Banana with Pumpkin Seeds", "time": "2 mins", "nutrients": "Magnesium, Tryptophan"}
            ],
            "joint stiffness": [
                {"name": "Turmeric Golden Milk", "time": "4 mins", "nutrients": "Anti-inflammatory"},
                {"name": "Walnuts + Dried Cranberries", "time": "1 min", "nutrients": "Omega-3, Antioxidants"},
                {"name": "Bone Broth Sip", "time": "2 mins", "nutrients": "Collagen, Minerals"}
            ],
            "mood variability": [
                {"name": "Dark Chocolate + Almonds", "time": "2 mins", "nutrients": "Magnesium, Mood Support"},
                {"name": "Greek Yogurt with Berries", "time": "2 mins", "nutrients": "Probiotics, Antioxidants"},
                {"name": "Hard-Boiled Egg", "time": "1 min", "nutrients": "Protein, B Vitamins"}
            ],
            "metabolic changes": [
                {"name": "Greek Yogurt with Nuts", "time": "2 mins", "nutrients": "Protein, Healthy Fats"},
                {"name": "String Cheese + Almonds", "time": "1 min", "nutrients": "Protein, Calcium"},
                {"name": "Avocado Toast", "time": "3 mins", "nutrients": "Protein, Fiber, Healthy Fats"}
            ]
        }

        snacks = []
        for symptom in symptoms_list:
            if symptom.lower() in quick_snacks:
                snacks.extend(quick_snacks[symptom.lower()])

        # Return unique snacks
        return list({s["name"]: s for s in snacks}.values())


def get_encouragement_message(symptoms, cycle_phase, life_phase=None):
    """Generate supportive, empowering messages"""
    messages = [
        "Your body is communicating its needs. By listening and nourishing yourself intentionally, you're practicing deep self-care.",
        "These symptoms are normal and temporary. Whole foods and mindful nutrition can help you feel more like yourself.",
        "You're not just treating symptoms—you're honoring your body's wisdom. Every nutrient choice is an act of self-love.",
        "Your body's rhythms are real, and your nutrition can work with them. You've got this.",
        "These symptoms aren't flaws—they're signals. Let's nourish your body with what it's asking for."
    ]

    base_message = messages[hash(str(symptoms)) % len(messages)]

    # Add life phase insights if menopausal
    if life_phase:
        life_phase_insights = {
            "perimenopause": " You're in an important transition—this is a time of becoming, not decline. Nourish yourself generously.",
            "menopause": " This phase is a natural part of your body's evolution. You deserve support, comfort, and foods that honor your strength.",
            "post-menopause": " You've navigated a major transition beautifully. Continue nourishing yourself with intention—your best years are ahead."
        }
        if life_phase.lower() in life_phase_insights:
            base_message += life_phase_insights[life_phase.lower()]
    # Add cycle phase insights for menstrual cycle
    elif cycle_phase:
        phase_insights = {
            "menstruation": " This is your body's renewal phase—prioritize iron and self-compassion.",
            "follicular": " Your energy is rising with your hormones. Eat lighter, brighter, and enjoy the upward momentum.",
            "ovulation": " You're at your peak! Honor this high-energy phase with nourishing meals that sustain your glow.",
            "luteal": " This is your cozy season. Warm foods, extra carbs, and self-nurturing are exactly what you need."
        }
        if cycle_phase.lower() in phase_insights:
            base_message += phase_insights[cycle_phase.lower()]

    return base_message


# Initialize engine
engine = SymptomNutritionEngine()
