# AscendCareer — Agent Rules

## Streamlit JavaScript Execution

**NEVER** inject `<script>` tags via `st.markdown(..., unsafe_allow_html=True)`.
Streamlit sanitizes these and renders the raw JS source code as visible text in the browser instead of executing it.

**ALWAYS** use `st.components.v1.html()` to execute JavaScript in Streamlit:

```python
import streamlit.components.v1 as components

# Step 1: Inject any HTML elements (canvas, divs, etc.) into the parent DOM
st.markdown(
    '<canvas id="my-canvas" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;"></canvas>',
    unsafe_allow_html=True,
)

# Step 2: Execute JS via components.html (properly executes scripts)
components.html("""
<script>
(function run() {
    // window.parent.document gives access to the Streamlit parent page
    // (works on localhost — same origin)
    const el = window.parent.document.getElementById('my-canvas');
    if (!el) { setTimeout(run, 50); return; }  // retry until element is ready

    // Use window.parent.innerWidth / window.parent.innerHeight for full-page sizing
    // ... your JS code here using el directly ...
})();
</script>
""", height=0, scrolling=False)
```

### Key Rules
- `components.html()` runs inside an iframe that shares the same origin as Streamlit (localhost)
- Use `window.parent.document` to access elements injected into the parent Streamlit page
- Always add a retry loop (`setTimeout(run, 50)`) — the element may not be in the DOM yet when the script first runs
- Use `window.parent.innerWidth` / `window.parent.innerHeight` for correct full-page dimensions (not the iframe's tiny dimensions)
- Set `height=0, scrolling=False` so the component iframe is completely invisible
- The JS body should NOT use a self-contained IIFE that calls `document.getElementById` — the element lookup happens in the outer wrapper that passes the element in
