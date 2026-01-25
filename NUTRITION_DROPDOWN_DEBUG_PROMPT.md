# Nutrition Tab Dropdown Debug & Fix Prompt

## Problem Statement
The nutrition tab has two related dropdowns that should have conditional visibility and behavior:
1. **Cycle Phase Dropdown** (`#cyclePhaseSelect`) - for menstrual cycle tracking
2. **Life Phase Dropdown** (`#lifePhaseSelect`) - for menopausal phase tracking

Currently, when users select menopause, perimenopause, or post-menopause in the Life Phase dropdown, the system should:
- ✅ Hide the Cycle Phase dropdown
- ❌ Hide menstrual cycle symptoms from the symptom grid
- ❌ Show menopausal-specific symptoms instead
- ❌ Display menopausal phase-specific recommendations

## Current Issue
The dropdowns toggle visibility, but the symptoms aren't changing based on the selection - menstrual cycle symptoms are still showing even when a menopausal phase is selected.

## Root Cause Analysis

### Location: `app.py` (lines ~3330-3400)
The `DOMContentLoaded` event listener handles the dropdown change events:

```javascript
lifePhaseSelect.addEventListener('change', function() {
    const selectedLifePhase = this.value;
    
    // ISSUE: This hides the dropdown but doesn't hide related UI elements
    // ISSUE: initializeNutritionSection() is called but may not be receiving symptoms correctly
    // ISSUE: No hiding of menstrual-specific symptom display
    
    initializeNutritionSection(selectedLifePhase || null);
});
```

### Issues to Fix

1. **Symptom Display Elements Not Hidden**
   - When menopausal phase is selected, there should be visual indicators that menstrual symptoms are unavailable
   - No mechanism to hide/show symptom descriptions that reference menstrual phases

2. **Symptom Grid Not Updating Properly**
   - `initializeNutritionSection()` fetches symptoms from backend
   - Needs verification that backend is returning menopausal symptoms correctly

3. **Missing UI Feedback**
   - No visual indication when switching between cycle and life phase
   - No tooltip or explanation showing "menstrual symptoms hidden for menopausal phase"

4. **Recommendation Display Not Linked**
   - When recommendations are retrieved, they should automatically adapt to show menopausal-specific advice
   - Need to ensure `getRecommendations()` properly sends both life_phase and cycle_phase to backend

## Code Locations to Review

### Frontend JavaScript (`app.py` embedded):
- **Lines ~3330-3400**: Life phase dropdown change listener
- **Lines ~3300-3330**: Cycle phase dropdown change listener  
- **Lines ~3193-3230**: `initializeNutritionSection()` function
- **Lines ~3233-3255**: `getRecommendations()` function
- **Lines ~3260-3320**: `displayRecommendations()` function

### Backend (`back/nutrition_api.py` or `back/nutrition_engine.py`):
- Verify `/api/nutrition/symptoms` endpoint returns correct symptoms based on `life_phase`
- Verify `/api/nutrition/recommendations` endpoint properly filters recommendations for menopausal phases

## Implementation Steps

### Step 1: Frontend - Add Symptom Container Management
- Identify the symptom grid container and its parent elements
- Add CSS classes to mark elements as "menstrual-only" or "menopausal-only"
- Create a function `updateSymptomDisplayMode(mode)` where mode is "menstrual" or "menopausal"

### Step 2: Frontend - Enhance Dropdown Change Listeners
For the **Life Phase** dropdown:
```javascript
lifePhaseSelect.addEventListener('change', function() {
    const selectedLifePhase = this.value;
    
    // Hide cycle phase selector
    cyclePhaseSelect.value = '';
    cyclePhaseDiv.style.display = 'none';
    
    // Update symptom display mode
    if (selectedLifePhase) {
        updateSymptomDisplayMode('menopausal');
        // Show menopausal-specific UI hint
        showPhaseHint('menopausal', selectedLifePhase);
    } else {
        updateSymptomDisplayMode('menstrual');
        hidePhaseHint();
    }
    
    // Reload symptoms for menopausal phase
    initializeNutritionSection(selectedLifePhase || null);
    
    // Clear previous recommendations
    clearRecommendations();
});
```

For the **Cycle Phase** dropdown:
```javascript
cyclePhaseSelect.addEventListener('change', function() {
    const selectedCyclePhase = this.value;
    
    // Hide life phase selector if cycle phase selected
    lifePhaseSelect.value = '';
    lifePhaseDiv.style.display = 'none';
    
    if (selectedCyclePhase) {
        updateSymptomDisplayMode('menstrual');
        showPhaseHint('menstrual', selectedCyclePhase);
    } else {
        updateSymptomDisplayMode('menstrual');
        hidePhaseHint();
    }
    
    // Reload menstrual symptoms
    initializeNutritionSection(null);
    
    // Clear previous recommendations
    clearRecommendations();
});
```

### Step 3: Frontend - Add Visual Feedback Functions
```javascript
function updateSymptomDisplayMode(mode) {
    const symptomGrid = document.getElementById('symptomGrid');
    if (mode === 'menopausal') {
        symptomGrid.classList.add('menopausal-mode');
        symptomGrid.classList.remove('menstrual-mode');
    } else {
        symptomGrid.classList.add('menstrual-mode');
        symptomGrid.classList.remove('menopausal-mode');
    }
}

function showPhaseHint(phase, selectedValue) {
    // Create or update a hint element showing current phase
    let hint = document.getElementById('phaseHint');
    if (!hint) {
        hint = document.createElement('div');
        hint.id = 'phaseHint';
        hint.style.cssText = 'padding: 12px 15px; margin-bottom: 15px; border-radius: 8px; font-size: 14px;';
        document.querySelector('.symptom-logger').insertBefore(hint, document.getElementById('symptomGrid'));
    }
    
    if (phase === 'menopausal') {
        hint.style.background = '#fff5f8';
        hint.style.borderLeft = '4px solid #ff9dbf';
        hint.innerHTML = `<strong>🌙 Menopausal Phase:</strong> ${selectedValue.charAt(0).toUpperCase() + selectedValue.slice(1)} — Showing menopausal symptoms only`;
    } else {
        hint.style.background = '#f5f8ff';
        hint.style.borderLeft = '4px solid #0284c7';
        hint.innerHTML = `<strong>🔄 Menstrual Cycle:</strong> ${selectedValue.charAt(0).toUpperCase() + selectedValue.slice(1).replace(/\d+.*/, '...')} — Showing menstrual cycle symptoms`;
    }
}

function hidePhaseHint() {
    const hint = document.getElementById('phaseHint');
    if (hint) hint.style.display = 'none';
}

function clearRecommendations() {
    const container = document.getElementById('recommendationsContainer');
    const snackContainer = document.getElementById('snacksContainer');
    if (container) {
        container.classList.remove('active');
        container.innerHTML = '';
    }
    if (snackContainer) {
        snackContainer.classList.remove('active');
        snackContainer.innerHTML = '';
    }
    selectedSymptoms = [];
}
```

### Step 4: Verify Backend Behavior
Check that `back/nutrition_engine.py` or `back/nutrition_api.py` has:
- `/api/nutrition/symptoms` - Returns different symptoms for `life_phase=menopause|perimenopause|post-menopause`
- `/api/nutrition/recommendations` - Filters recommendations to menopausal-specific advice when `life_phase` is set

Expected behavior:
```
GET /api/nutrition/symptoms?life_phase=menopause
→ Returns menopausal symptoms (hot flashes, night sweats, mood changes, etc.)

GET /api/nutrition/symptoms  (no life_phase)
→ Returns menstrual cycle symptoms (cramps, bloating, fatigue, etc.)

POST /api/nutrition/recommendations
  body: { symptoms: [...], life_phase: "menopause", cycle_phase: null }
→ Returns menopausal-specific food recommendations
```

### Step 5: Add CSS for Visual Mode Indication
Add to the HTML template styles:
```css
.symptom-logger.menopausal-mode {
    /* Optional: highlight when in menopausal mode */
    border: 1px solid #ffc0d3;
}

.symptom-btn {
    transition: all 0.3s ease;
}

#phaseHint {
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

## Testing Checklist

- [ ] **Dropdown Toggle**: Selecting menopause hides cycle dropdown ✓
- [ ] **Dropdown Toggle**: Selecting cycle phase hides life phase dropdown ✓
- [ ] **Symptoms Load**: Symptoms change when switching between menopause/menstrual ✓
- [ ] **Visual Feedback**: Phase hint appears showing current selection ✓
- [ ] **Recommendations**: Getting recommendations returns menopausal-specific advice ✓
- [ ] **Recommendations**: Menopausal recommendations don't reference menstrual phases ✓
- [ ] **Clear State**: Switching phases clears previous recommendations ✓
- [ ] **Default State**: Page loads with "Not applicable" selected, showing menstrual symptoms ✓
- [ ] **Quick Snacks**: Quick snacks button works with menopausal symptoms ✓

## Success Criteria

When **menopause, perimenopause, or post-menopause** is selected:
1. ✅ Cycle phase dropdown is hidden and cleared
2. ✅ Symptom grid displays menopausal-specific symptoms (NOT menstrual)
3. ✅ Visual indicator shows "Menopausal Phase" with the selected option
4. ✅ Recommendations are menopausal-appropriate
5. ✅ No references to menstrual cycle phases in recommendations
6. ✅ Snack suggestions are appropriate for menopausal phase

## Debug Commands

To test backend behavior:
```bash
# Test menstrual symptoms
curl -X POST http://localhost:5001/api/nutrition/symptoms \
  -H "Content-Type: application/json" \
  -d '{"life_phase": null}'

# Test menopausal symptoms  
curl -X POST http://localhost:5001/api/nutrition/symptoms \
  -H "Content-Type: application/json" \
  -d '{"life_phase": "menopause"}'

# Test recommendations with menopausal phase
curl -X POST http://localhost:5001/api/nutrition/recommendations \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["hot_flashes", "mood_changes"], "cycle_phase": null, "life_phase": "menopause"}'
```

## Files to Modify

1. **`app.py`** - Frontend JavaScript section (embedded HTML template)
   - Update lifePhaseSelect change listener (lines ~3330-3370)
   - Update cyclePhaseSelect change listener (lines ~3370-3410)
   - Add new helper functions: `updateSymptomDisplayMode()`, `showPhaseHint()`, `hidePhaseHint()`, `clearRecommendations()`

2. **`back/nutrition_engine.py` or `back/nutrition_api.py`** (if needed)
   - Verify symptoms endpoint properly distinguishes menopausal vs menstrual
   - Verify recommendations endpoint filters appropriately
   - Consider adding fallback for unrecognized life_phase values

## Notes
- The backend should already handle life_phase filtering in `initializeNutritionSection()`
- The dropdown logic is present but incomplete in terms of visual feedback and symptom display
- Main issue is disconnect between dropdown value and symptom display content
