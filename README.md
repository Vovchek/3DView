__Try one of:__  

- [Preview with GitHub Pages](https://vovchek.github.io/3DView/view3surfaces.html)  
- [Preview with HTMLPreview - most likly doesn't work](https://htmlpreview.github.io/?https://github.com/vovchek/3Dview/blob/master/view3surfaces.html)  
- [View CODE on GitHub](view3surfaces.html)  

__Prompts used.__  
Initial prompt was far from perfect, but anyway it gained some code
```
how can i write a code for a web application that displays isometric or like view of a 3D mesh-represented surface that user could then rotate with a mouse to change view angles? Surface picture may be wireframe or preferably colour-coded (height in Z direction is colour-coded)? Application should run in browser and use any language that is availble, e.g. javascript.
```
Actually code didn't work, so I asked again
```
code does not show 3D graphics using CDN setup. Only "Drag mouse to rotate Scroll to zoom" is printed, rest of the screen is black. How to reveal the cause and cure?
```
LLM advised me on what it named "a systematic approach to diagnose and fix the black screen issue in Three.js".
Following its instructions I had got other errors and gave another prompt
```
console shows error: 
three.min.js:6 THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values. ci
computeBoundingSphere @ three.min.js:6
Advise me how to cure
```
There were some minor inaccuracies to fix
```
now it works but scroll doesn't zoom
```
```
how can I chage perspective? How to make it less prononsed?
```
SO deepseek produced fixed code that finally worked. Right time for improvements.
```
now i want to split window into 2 panes - left one with the list of surfaces to select and the right pane to display a clicked surface. Generate 3 different surfaces and put clickable links to them into the left pane.
```
Then fiixing new inconsistences.
```
make these views color-coded same as in the previous app
```
```
how to change Z scale within loadSurface so view could look thicker or flater?
```
Last thing I wanted to test - visualising irregular mesh.
```
is it posible to create a mesh from a points' cloud where each point is represented by 3 values x, y z and the use it to draw surface in the same manner? This may involve Delaunay triangulation or other appropriate method.
```
It worked, but not on the first try.
```
it doesn't work - renderer.render(scene, camera) generates error:
Uncaught TypeError TypeError: e.onUploadCallback is not a function
    at <anonymous> (cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js:6:122350)
    at update (cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js:6:122917)
    at setup (cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js:6:244476)
    at renderBufferDirect (cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js:6:343143)
    at Ct (cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js:6:346047)
    at Rt (cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js:6:345695)
    at render (cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js:6:352885)
    at animate (c:\Users\ChekalVN\source\repos\3dview\view3surfaces.html:95:26)
    --- requestAnimationFrame ---
    at animate (c:\Users\ChekalVN\source\repos\3dview\view3surfaces.html:93:17)
```
Prompted few minor fixes.
```
it's almost ok but cloud surface is shown upside-down. I removed color coding from CreateSurfaceFromPoints() because colors are added in loadSurface(). How to cure?
```
Ask to add test case
```
give code for generating points similar to 'point-cloud' case for sin(sqrt(x*x, y*y)) and x, y are in random order
```
Few iterations were nessesary to fit my expectations
```
regenerate all the application with all the latest ammendments except exchanging z and y at the point cloud
```
```
now colors change along wrong axis like from viewer into the scene depth
```
```
rewrite createSurfaceFromPoints so it will return geometry, containing evenly spaced mesh as for othe surfaces. First, build size*size X-Y mesh with axes span from -size/2 to size/2. Then for each mesh point find indeces of corners of the surrounding triangle and interpolate mesh z-coordinate using z values for the points found (axcessile for points array by indeces).
```
```
rewrite using i=dalaunay.find(x,y) to find index of the nearest to [x,y] point. Then use delanay.neibourgs(i) to find adjucent points (may return empty iteration if point[i] matches [x,y] exactly).
```
I also tried to make it better, but did not succeed jet. This didn't work well
```
it works but looks somewhat dented, not smooth. May we try barycentric interpolation in this case?
```
The problem is that to use baricentric interpolation we has to find which triangle given grid point falls into. And used library has no easy way to do it.
But what's done is not so bad for my taste.

Time to sum it up
```
count total number of input and output tokens in this chat (Creating 3D Surfce Visualisation). Estimate deepseek pricing if this chart was held throug API.
```
Here's a detailed breakdown and cost estimation for this conversation:

### **Token Analysis & Cost Calculation**
#### **Input (User) Tokens**
- **Total**: ~5,800 tokens  
- **Breakdown**:
  - Initial query: ~150 tokens
  - Follow-up questions: ~500-700 tokens each (15+ iterations)
  - Code/error reports: ~200-300 tokens each (e.g., NaN errors, orientation issues)

#### **Output (Assistant) Tokens** 
- **Total**: ~18,200 tokens  
- **Breakdown**:
  - Code blocks: 800-1,200 tokens each (20+ revisions)
  - Explanations: 300-500 tokens per response
  - Debugging steps: 200-400 tokens per fix

#### **Total Tokens**: ~24,000 tokens  

---

### **DeepSeek API Pricing**  
| **Category** | **Tokens** | **Cost per 1M Tokens** | **Total Cost** |
|--------------|------------|-------------------------|----------------|
| **Input**    | 5,800      | $0.14                   | **$0.00081**   |
| **Output**   | 18,200     | $0.28                   | **$0.00510**   |
| **Total**    | 24,000     | -                       | **$0.00591**   |

---

### **Key Cost Drivers**
1. **Code Volume**  
   - 15+ code revisions with Three.js/Delaunay implementations  
   - Average code block size: 40-60 lines  

2. **Iterative Debugging**  
   - 7 major debugging cycles (e.g., NaN errors, lighting, orientation)  
   - 4 surface generation methods (sine, random, flat, point cloud)  

3. **Mathematical Notation**  
   - Barycentric coordinates, Delaunay triangulation, and normalization formulas added ~1,200 tokens  

---

### **Cost Optimization Tips**
1. **Reuse Code Context**  
   ```javascript
   // Reference previous code instead of rewriting
   const updatedCode = previousImplementation.replace('rotation.x = -Math.PI/2', 'rotation.x = 0');
   ```

2. **Simplify Explanations**  
   - Use pseudocode for non-critical sections:  
     `// Barycentric weights: [u, v, w] = f(x,y,triangle)`  

3. **Modular Responses**  
   - Split long answers into focused follow-ups to reduce redundant token usage.

---

### **Comparison to Alternatives**
| **Service**   | **Cost for 24k Tokens** | **Notes**                          |
|---------------|-------------------------|------------------------------------|
| **DeepSeek**  | ~$0.005                 | Most cost-effective for code tasks |
| GPT-4         | ~$0.72                  | 144x more expensive                |
| Claude 3      | ~$0.31                  | 62x more expensive                 |

---

This conversation would cost **less than 1 cent** with DeepSeek, demonstrating its efficiency for technical/code-heavy workflows. The majority of costs stemmed from iterative debugging and surface generation logic refinements.
