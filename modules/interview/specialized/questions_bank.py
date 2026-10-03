"""
AchieveHire — Specialized Interview Question Bank & Dynamic Generator
Maintains curated technical question pools across standard specializations
and dynamically generates round-specific questions for manually entered specializations.
Supports English, Hindi, and natural conversational Indian Hinglish.
"""

from typing import List, Dict, Optional, Any
import hashlib
from modules.interview.specialized.models import QuestionItem


# ─────────────────────────────────────────────────────────────────────────────
# Introduction & Closing Standard Questions
# ─────────────────────────────────────────────────────────────────────────────

INTRO_QUESTION_ROUND1 = QuestionItem(
    id="intro_r1_01",
    text_en="Please introduce yourself.",
    text_hi="कृपया अपना संक्षिप्त परिचय दीजिए और अपनी तकनीकी पृष्ठभूमि के बारे में बताइए।",
    text_hinglish="Please introduce yourself aur apne background aur technical experience ke baare mein briefly bataiye.",
    difficulty="Easy",
    specialization="General",
    category="Introduction & Background",
    expected_points=[
        "Brief professional identity / educational background",
        "Key technical competencies and chosen specialization focus",
        "Relevant projects, internship, or work experience",
        "Career trajectory and enthusiasm for continuous learning",
    ],
    correct_answer=(
        "A structured elevator pitch: (1) Current role/academics, (2) Core technical strengths and specialization, "
        "(3) Significant project/experience highlights with quantified impact, (4) Career aspiration aligned with the interview."
    ),
    better_possible_answer=(
        "\"Hi, my name is [Name]. I'm a software developer with a strong focus on [Specialization]. "
        "Over the past couple of years, I've built [key project/system] where I engineered [core feature] resulting in [quantified impact]. "
        "My core strengths include [Skill 1], [Skill 2], and designing robust architectures. "
        "I'm excited to be here today to discuss my technical depth and how I approach engineering problems.\""
    ),
    is_intro=True,
)

INTRO_QUESTION_ROUND4 = QuestionItem(
    id="intro_r4_01",
    text_en="Please introduce yourself.",
    text_hi="कृपया अपना परिचय दीजिए—आपकी मुख्य तकनीकी शक्तियों, हालिया उपलब्धियों और इंजीनियरिंग दृष्टिकोण को संक्षेप में साझा करें।",
    text_hinglish="Please introduce yourself aur apne core engineering strengths, recent technical achievements, aur problem-solving approach ko highlight kijiye.",
    difficulty="Final",
    specialization="General",
    category="Introduction & Leadership Evolution",
    expected_points=[
        "Polished, concise executive-style introduction",
        "Clear demonstration of technical mastery and specialization impact",
        "Systemic problem-solving mindset and leadership/collaboration maturity",
        "Evolution of communication confidence compared to foundational rounds",
    ],
    correct_answer=(
        "An executive, impact-oriented summary: Concise identity, high-level technical domain mastery, "
        "key architectural contributions, and strategic engineering mindset."
    ),
    better_possible_answer=(
        "\"Hello! I am [Name], a software engineer specializing in [Specialization]. "
        "I thrive on architecting scalable systems and solving complex domain challenges. "
        "Recently, I designed and optimized [System/Project], improving latency by 35% and streamlining data consistency. "
        "Beyond writing clean, maintainable code, I value clear communication, architectural trade-offs, and iterative improvement. "
        "I'm eager to tackle today's final technical and architectural discussion.\""
    ),
    is_intro=True,
)

CLOSING_QUESTION_ROUND4 = QuestionItem(
    id="closing_r4_01",
    text_en="Do you have any questions for us?",
    text_hi="क्या आपके पास हमारे लिए या इंजीनियरिंग टीम के लिए कोई सवाल है?",
    text_hinglish="We're approaching the end of our session. Do you have any questions for us regarding the technical architecture or engineering culture?",
    difficulty="Final",
    specialization="General",
    category="Candidate Closing Inquiry",
    expected_points=[
        "Thoughtful question regarding engineering challenges, tech stack scalability, or system design decisions",
        "Inquiry about deployment workflows, code review standards, or team growth philosophy",
        "Clear interest in technical impact rather than merely administrative queries",
    ],
    correct_answer=(
        "Engaging, high-impact inquiry demonstrating genuine technical curiosity, curiosity about the team's engineering practices, "
        "or architectural scalability roadmaps."
    ),
    better_possible_answer=(
        "\"Yes, thank you! I'd love to learn more about how your team approaches [architectural challenge / tech stack migration] "
        "and what the engineering feedback loop looks like when shipping high-concurrency features to production.\""
    ),
    is_closing=True,
)


def get_self_intro_question(round_num: int = 1) -> QuestionItem:
    """Returns the standardized self-introduction question for Round 1 or Round 4."""
    if round_num == 4:
        return INTRO_QUESTION_ROUND4
    return INTRO_QUESTION_ROUND1


def get_closing_candidate_inquiry() -> QuestionItem:
    """Returns the candidate-led closing question for Round 4."""
    return CLOSING_QUESTION_ROUND4


CURATED_QUESTIONS: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "python": {
        "Easy": [
            {
                "id": "py_e1",
                "text_en": "What is the difference between mutable and immutable data types in Python, and why does it matter?",
                "text_hi": "Python में mutable और immutable data types में क्या अंतर है, और यह मेमोरी और परफॉर्मेंस के लिए क्यों महत्वपूर्ण है?",
                "text_hinglish": "Python mein mutable aur immutable data types mein kya difference hota hai, aur memory management ke liye yeh kyun important hai?",
                "category": "Core Data Structures",
                "expected_points": ["Lists/dicts/sets are mutable; tuples/strings/ints are immutable", "Object ID and memory reallocation upon modification", "Default argument mutation bug prevention"],
                "correct_answer": "Mutable objects (like lists, dicts, sets) can be modified in-place without changing their memory ID. Immutable objects (like ints, floats, strings, tuples) cannot be altered after creation; any modification produces a new object in memory.",
                "better_possible_answer": "\"In Python, mutable objects like lists and dictionaries can have their contents modified in-place without changing their memory address. In contrast, immutable types like strings and tuples create an entirely new object in memory whenever modified. This distinction is crucial when passing arguments to functions—especially avoiding mutable default arguments—and when designing dictionary keys, which require immutable, hashable types.\""
            },
            {
                "id": "py_e2",
                "text_en": "How do lists and tuples differ in Python regarding memory usage, performance, and use-cases?",
                "text_hi": "Python में lists और tuples में मेमोरी उपयोग, परफॉर्मेंस और उपयोग के मामलों में क्या अंतर है?",
                "text_hinglish": "Python mein lists aur tuples memory, performance aur use-cases ke terms mein kaise differ karte hain?",
                "category": "Data Structures & Performance",
                "expected_points": ["Lists are dynamic and have over-allocation overhead", "Tuples are fixed size and lightweight", "Tuples can be used as dictionary keys (hashable)"],
                "correct_answer": "Lists are mutable and dynamically sized, which requires Python to allocate excess memory buffer for future appends. Tuples are immutable and fixed-size, resulting in lower memory footprint and faster iteration.",
                "better_possible_answer": "\"Lists are mutable dynamic arrays designed for homogeneous sequences that change size. Tuples are immutable fixed-length collections that have less memory overhead because Python doesn't need to allocate spare capacity for resizing. Tuples are also hashable, making them suitable as dictionary keys and set elements.\""
            },
            {
                "id": "py_e3",
                "text_en": "Explain what list comprehensions and generator expressions are, and when you would prefer one over the other.",
                "text_hi": "List comprehensions और generator expressions क्या हैं, और आप एक की तुलना में दूसरे को कब प्राथमिकता देंगे?",
                "text_hinglish": "List comprehensions aur generator expressions kya hote hain, aur memory efficiency ke liye kisse kab prefer karna chahiye?",
                "category": "Iteration & Memory Optimization",
                "expected_points": ["List comprehensions build the whole list in memory immediately (eager)", "Generator expressions evaluate lazily on-demand using iterator protocol", "Use generators for large or infinite streams to save RAM"],
                "correct_answer": "List comprehensions construct the entire collection eagerly in memory surrounded by brackets []. Generator expressions use parentheses () and evaluate items lazily on demand using the iterator protocol, which saves substantial RAM when dealing with large datasets.",
                "better_possible_answer": "\"List comprehensions are concise syntactic sugar to create a complete list in memory eagerly. Generator expressions, created with parentheses, return a generator object that yields elements one at a time on demand. I prefer list comprehensions when I need random access, length, or multiple iterations over small datasets, and generator expressions for large data pipelines to keep memory footprint minimal (O(1) memory).\""
            },
            {
                "id": "py_e4",
                "text_en": "What is the Global Interpreter Lock (GIL) in CPython, and what impact does it have on multi-threaded programs?",
                "text_hi": "CPython में Global Interpreter Lock (GIL) क्या है, और यह मल्टी-थ्रेडेड प्रोग्राम्स को कैसे प्रभावित करता है?",
                "text_hinglish": "CPython mein Global Interpreter Lock (GIL) kya hai, aur yeh CPU-bound multi-threading ko kaise affect karta hai?",
                "category": "Concurrency & Python Internals",
                "expected_points": ["GIL is a mutex protecting Python bytecode execution", "Allows only one native thread to execute Python bytecode at a time", "CPU-bound tasks require multiprocessing or C-extensions, while I/O-bound tasks benefit from threading"],
                "correct_answer": "The GIL is a mutex in CPython that ensures only one thread executes Python bytecode at any given moment. This prevents CPU-bound multi-threaded Python code from achieving true parallel execution across multiple cores. For I/O-bound tasks, the GIL is released during system calls.",
                "better_possible_answer": "\"The GIL is a mutex mechanism in CPython designed to prevent race conditions in Python's reference-counting memory management. As a result, only one thread can execute Python bytecode at a time. While multi-threading still helps I/O-bound tasks where threads wait on network or disk, CPU-bound tasks should use the multiprocessing module or asynchronous event loops (asyncio) to achieve true parallelism across CPU cores.\""
            },
        ],
        "Moderate": [
            {
                "id": "py_m1",
                "text_en": "How do Python decorators work under the hood, and how would you implement a decorator that accepts custom configuration arguments?",
                "text_hi": "Python decorators आंतरिक रूप से कैसे काम करते हैं, और आप ऐसा decorator कैसे बनाएंगे जो custom arguments स्वीकार करता हो?",
                "text_hinglish": "Python decorators internally kaise work karte hain, aur parameters accept karne wala custom decorator aap kaise implement karenge?",
                "category": "Advanced Language Features & Metaprogramming",
                "expected_points": ["First-class functions / closures wrapping target callable", "Triple-nested function pattern for parameterized decorators", "functools.wraps to preserve function metadata (__name__, __doc__)"],
                "correct_answer": "Decorators are higher-order functions that take a function as input, wrap it inside a closure to add pre/post behavior, and return the wrapped function. Parameterized decorators require a 3-tier function structure where the outermost function accepts arguments, the middle receives the target function, and the innermost handles invocation.",
                "better_possible_answer": "\"Decorators leverage Python's first-class functions and closures. Syntactically, @decorator is equivalent to func = decorator(func). To pass arguments to a decorator, we write a decorator factory—a function returning the actual decorator, requiring three nested functions. We always apply @functools.wraps(func) to preserve the original function's docstring and signature metadata.\""
            },
            {
                "id": "py_m2",
                "text_en": "Explain Python's memory management model: How does reference counting combine with the generational garbage collector to handle cyclic references?",
                "text_hi": "Python का मेमोरी मैनेजमेंट मॉडल कैसे काम करता है: Reference counting और generational garbage collection चक्रीय संदर्भों (cyclic references) को कैसे हल करते हैं?",
                "text_hinglish": "Python ka memory management model explain kijiye: Reference counting aur generational garbage collector cyclic references ko kaise handle karte hain?",
                "category": "Memory Management & Internals",
                "expected_points": ["Primary mechanism is reference counting (ob_refcnt)", "Deallocation occurs immediately when refcount reaches 0", "Generational GC (Gen 0, 1, 2) detects unreferenced circular reference graphs"],
                "correct_answer": "CPython primarily uses reference counting for immediate cleanup when an object's reference drops to zero. However, self-referential or circular objects never reach zero reference count. To resolve this, Python runs a generational garbage collector (Gen 0, 1, 2) that periodically traverses container objects, detects isolated reference cycles, and frees their memory.",
                "better_possible_answer": "\"CPython uses a two-tier memory manager: reference counting handles 99% of deallocations instantaneously as soon as an object's refcount drops to zero. To solve circular references where objects reference each other, Python incorporates a heuristic generational cyclic garbage collector. Objects start in Generation 0; survivors of collection cycles are promoted to Generation 1 and 2, which are checked less frequently, optimizing throughput.\""
            },
            {
                "id": "py_m3",
                "text_en": "What are *args and **kwargs in Python, and how does dictionary unpacking interact with keyword-only arguments?",
                "text_hi": "*args और **kwargs क्या हैं, और keyword-only arguments के साथ इनका क्या संबंध है?",
                "text_hinglish": "*args aur **kwargs ka exact usage kya hai, aur keyword-only arguments (* syntax) ke saath yeh kaise interact karte hain?",
                "category": "Function Signatures & Unpacking",
                "expected_points": ["*args packs positional arguments into a tuple", "**kwargs packs keyword arguments into a dict", "Bare * in signature forces subsequent parameters to be passed strictly by keyword"],
                "correct_answer": "*args gathers arbitrary positional parameters into a tuple, while **kwargs collects arbitrary keyword arguments into a dictionary. Placing a bare * in a parameter list forces all following parameters to be passed strictly as keyword arguments, preventing accidental positional misplacement.",
                "better_possible_answer": "\"*args captures variable positional arguments into a tuple, and **kwargs captures keyword arguments into a dictionary. In modern Python, you can define keyword-only arguments by placing parameters after *args or after a bare asterisk (*). This guarantees API safety by forcing callers to name their parameters explicitly, preventing bugs in complex function calls.\""
            },
        ],
        "Hard": [
            {
                "id": "py_h1",
                "text_en": "How does the asyncio event loop work in Python, and how does cooperative multitasking differ from OS-level preemptive threading?",
                "text_hi": "Python में asyncio event loop कैसे काम करता है, और cooperative multitasking OS-level preemptive threading से किस प्रकार भिन्न है?",
                "text_hinglish": "Python mein asyncio event loop kaise operate karta hai, aur cooperative multitasking vs preemptive OS threading mein architectural trade-offs kya hain?",
                "category": "Asynchronous Architecture & Event Loops",
                "expected_points": ["Single-threaded event loop running coroutines based on generators/future objects", "Cooperative: coroutines yield control via 'await' during I/O", "Preemptive threading: OS scheduler forcibly context switches threads with lock overhead"],
                "correct_answer": "asyncio uses a single-threaded cooperative event loop. Coroutines explicitly yield control back to the event loop using 'await' while waiting on non-blocking I/O operations (sockets, files, timers). Preemptive OS threading relies on the OS kernel scheduler to interrupt threads arbitrarily, incurring lock contention and context-switching overhead.",
                "better_possible_answer": "\"asyncio implements cooperative multitasking on a single thread using an event loop and epoll/kqueue system selectors. When a coroutine hits an 'await', it yields execution back to the loop, allowing other ready coroutines to proceed. Unlike OS threads that require locking primitives and incur thread stack overhead (~8MB per thread), asyncio handles tens of thousands of concurrent I/O connections in a single process with minimal memory overhead.\""
            },
            {
                "id": "py_h2",
                "text_en": "Explain Python's Metaclasses and the __new__ versus __init__ lifecycle during class instantiation and class creation.",
                "text_hi": "Python के Metaclasses क्या हैं, और class creation और instantiation के दौरान __new__ और __init__ के lifecycle में क्या अंतर है?",
                "text_hinglish": "Python Metaclasses aur __new__ vs __init__ lifecycle ko explain kijiye: class creation aur object instantiation time par kya sequence follow hota hai?",
                "category": "Metaprogramming & Object Lifecycle",
                "expected_points": ["Classes are instances of metaclasses (default is 'type')", "__new__ is the static constructor that creates and returns the instance", "__init__ is the initializer that configures attributes on the existing instance"],
                "correct_answer": "In Python, classes themselves are objects created by metaclasses (by default, 'type'). During object instantiation, __new__ is called first to allocate memory and construct the instance; then __init__ receives that instance to initialize its attributes. Metaclasses intercept class construction itself, allowing validation, registration, and modification of classes before they exist.",
                "better_possible_answer": "\"Metaclasses are the 'classes of classes'—they define how classes themselves are constructed. In the object lifecycle, __new__ is the true constructor: a static method responsible for allocating and returning a new instance. Once created, __init__ receives this instance as 'self' to set initial attributes. Metaclasses use their own __new__ to inspect, modify, or enforce API contracts on class definitions at module import time.\""
            },
        ],
        "Final": [
            {
                "id": "py_f1",
                "text_en": "Design a thread-safe, high-concurrency LRU (Least Recently Used) cache in Python with O(1) read and write time complexity. What data structures and synchronization primitives would you select?",
                "text_hi": "Python में O(1) read और write time complexity वाला thread-safe high-concurrency LRU Cache कैसे डिज़ाइन करेंगे? कौन से data structures और synchronization locks उपयोग करेंगे?",
                "text_hinglish": "Python mein O(1) read/write time complexity ke saath thread-safe high-concurrency LRU Cache kaise architect karenge? Konsi data structures aur locks use karenge?",
                "category": "System Architecture & Data Structures",
                "expected_points": ["Doubly Linked List + Hash Map (or collections.OrderedDict)", "O(1) lookup via Hash Map and O(1) node repositioning via Doubly Linked List", "threading.Lock or Reader-Writer lock (threading.RLock) for thread safety"],
                "correct_answer": "An LRU Cache combines a Hash Map (for O(1) key-to-node lookups) and a Doubly Linked List (for O(1) node additions, evictions, and moving accessed items to the head). In multi-threaded environments, access to the dictionary and linked list pointers must be protected by an RLock or partitioned bucket locks to minimize contention.",
                "better_possible_answer": "\"To achieve O(1) for both get and put, I use a Hash Map paired with a Doubly Linked List containing sentinel head and tail nodes. The map stores key -> Node references. On access, the node is spliced out and moved to head in O(1). When capacity is exceeded, the node before tail is evicted in O(1). For thread safety, I wrap critical pointer mutations inside a threading.RLock, or partition the cache into multiple striped shards to reduce lock contention under high concurrency.\""
            },
            {
                "id": "py_f2",
                "text_en": "How do Python context managers work at the bytecode level, and how would you handle suppressed exceptions in __exit__ without masking unexpected errors?",
                "text_hi": "Python context managers bytecode level पर कैसे काम करते हैं, और __exit__ में unexpected errors को mask किए बिना exceptions को कैसे handle करते हैं?",
                "text_hinglish": "Context managers (__enter__ aur __exit__) ke internal semantics kya hain, aur specific exceptions ko suppress karte waqt general bugs ko suppress hone se kaise bachaenge?",
                "category": "Resource Safety & Exception Protocols",
                "expected_points": ["__enter__() acquires resource; __exit__(exc_type, exc_val, exc_tb) handles teardown", "Returning True from __exit__ suppresses the exception", "Only suppress explicitly expected exception types; otherwise return False or None"],
                "correct_answer": "Context managers implement the Context Management Protocol via __enter__ and __exit__. When entering a 'with' block, __enter__ is called. Upon exit (normal or exceptional), __exit__ receives exc_type, exc_val, and traceback. If __exit__ returns True, Python suppresses the exception; returning False allows it to propagate. To avoid masking real bugs, check if isinstance(exc_val, ExpectedException) before returning True.",
                "better_possible_answer": "\"A context manager ensures deterministic resource cleanup via __enter__ and __exit__. When an exception occurs within the 'with' block, __exit__(exc_type, exc_val, exc_tb) is invoked. If __exit__ returns True, the exception is swallowed; otherwise it propagates. Best practice dictates checking `if exc_type and issubclass(exc_type, SpecificKnownError): return True`, ensuring unanticipated exceptions like KeyErrors or TypeErrors bubble up cleanly for debugging.\""
            },
        ],
    },
    "java": {
        "Easy": [
            {
                "id": "java_e1",
                "text_en": "What is the difference between JDK, JRE, and JVM in Java architecture?",
                "text_hi": "Java आर्किटेक्चर में JDK, JRE और JVM में क्या अंतर है?",
                "text_hinglish": "Java architecture mein JDK, JRE aur JVM mein kya differences hain?",
                "category": "Java Fundamentals",
                "expected_points": ["JVM executes bytecode and manages memory", "JRE provides JVM + standard libraries to run programs", "JDK provides JRE + compiler (javac) + developer tools"],
                "correct_answer": "JVM (Java Virtual Machine) executes compiled bytecode. JRE (Java Runtime Environment) bundles the JVM along with core class libraries to run applications. JDK (Java Development Kit) includes the JRE plus development tools like the javac compiler and debugger.",
                "better_possible_answer": "\"JVM is the platform-dependent execution engine that runs compiled bytecode. JRE is the runtime bundle containing the JVM and standard libraries needed to execute Java apps. JDK is the complete development kit containing the JRE, compiler (javac), documentation tools, and debuggers necessary to write and build Java software.\""
            },
            {
                "id": "java_e2",
                "text_en": "Explain the four core principles of Object-Oriented Programming (OOP) with concise real-world examples in Java.",
                "text_hi": "Object-Oriented Programming (OOP) के चार मुख्य सिद्धांतों को Java के उदाहरणों के साथ समझाइए।",
                "text_hinglish": "OOPs ke 4 core pillars—Encapsulation, Abstraction, Inheritance, Polymorphism—ko Java perspective se explain kijiye.",
                "category": "Object-Oriented Principles",
                "expected_points": ["Encapsulation (data hiding with getters/setters)", "Abstraction (interfaces/abstract classes hiding complexity)", "Inheritance (code reuse with extends)", "Polymorphism (method overloading & overriding)"],
                "correct_answer": "Encapsulation bundles data and methods together with access control. Abstraction hides internal complexity through interfaces and abstract classes. Inheritance enables code reuse and hierarchical modeling. Polymorphism allows methods to behave differently based on the runtime object.",
                "better_possible_answer": "\"The 4 OOP pillars in Java are: 1. Encapsulation: Protecting internal object state using private fields and public getters/setters. 2. Abstraction: Exposing only essential contracts using Interfaces while hiding implementation. 3. Inheritance: Reusing and extending parent class functionality using the extends keyword. 4. Polymorphism: Allowing dynamic method dispatch where a parent reference invokes the overridden child method at runtime.\""
            },
        ],
        "Moderate": [
            {
                "id": "java_m1",
                "text_en": "How does HashMap work internally in Java 8+, specifically regarding hash collisions and the treeification threshold?",
                "text_hi": "Java 8+ में HashMap आंतरिक रूप से कैसे काम करता है, विशेष रूप से hash collisions और treeification (Red-Black Tree) के संबंध में?",
                "text_hinglish": "Java 8+ mein HashMap internal working explain kijiye: hash collisions ke case mein LinkedList kab Red-Black Tree mein convert hoti hai?",
                "category": "Collections & Data Structures",
                "expected_points": ["Array of Node buckets (Node<K,V>[])", "Hash calculation with bit-shifting: (n-1) & hash", "Collision handling via LinkedList; transforms to Red-Black Tree when bucket size >= 8"],
                "correct_answer": "Java HashMap uses an array of buckets. Keys are hashed, and their bucket index is determined using bitwise AND. When collisions occur, entries are stored in a linked list. If a single bucket exceeds 8 entries (TREEIFY_THRESHOLD) and table capacity >= 64, the linked list converts into a balanced Red-Black Tree, improving collision lookup from O(n) to O(log n).",
                "better_possible_answer": "\"In Java 8, HashMap is backed by an array of Node buckets. The index is calculated via `(n - 1) & hash`. When two keys collide, they form a linked list in that bucket. If the list length reaches 8 and total capacity is at least 64, Java converts that bucket into a Red-Black Tree (TreeNode), reducing worst-case lookup from O(n) to O(log n). When elements decrease below 6, it reverts back to a linked list.\""
            },
        ],
        "Hard": [
            {
                "id": "java_h1",
                "text_en": "Explain the Java Memory Model: Stack vs Heap, Metaspace, and how Garbage Collectors (like G1 GC or ZGC) manage young and old generations.",
                "text_hi": "Java Memory Model समझाइए: Stack vs Heap, Metaspace, और Garbage Collectors (जैसे G1 GC) generations को कैसे मैनेज करते हैं?",
                "text_hinglish": "Java Memory Model explain kijiye: Stack vs Heap allocation, Metaspace, aur G1 GC / ZGC garbage collection mechanics kya hain?",
                "category": "JVM Architecture & Memory",
                "expected_points": ["Stack stores thread-specific primitive variables & reference pointers", "Heap stores actual object instances shared across threads", "Generational GC: Eden, Survivor (S0/S1), Tenured/Old generation"],
                "correct_answer": "Stack memory is thread-local and stores method call frames, local primitives, and object references. Heap memory stores all object instances and is managed by the Garbage Collector. Modern collectors like G1 GC partition the heap into equal regions categorized dynamically into Eden, Survivor, and Old generations, targeting regions with the highest garbage density to minimize stop-the-world pauses.",
                "better_possible_answer": "\"Stack memory is thread-local, extremely fast, and automatically reclaimed upon method exit. The Heap is shared across threads and holds all object allocations. Metaspace stores class metadata in native memory. Modern G1 GC divides the heap into thousands of equal regions rather than contiguous generations. It tracks live objects concurrently and prioritizes collecting regions with the most garbage ('Garbage-First') to meet user-configured latency SLA targets.\""
            },
        ],
        "Final": [
            {
                "id": "java_f1",
                "text_en": "How do volatile, synchronized, and java.util.concurrent locks (like ReentrantLock and StampedLock) differ in ensuring atomicity, visibility, and ordering in Java?",
                "text_hi": "Java में concurrency के दौरान atomicity, visibility और instruction ordering को सुनिश्चित करने में volatile, synchronized और ReentrantLock में क्या अंतर है?",
                "text_hinglish": "Multi-threading mein volatile vs synchronized vs ReentrantLock ka difference explain kijiye: Atomicity, Visibility aur Memory Barriers kaise enforce hote hain?",
                "category": "Concurrency & Multi-Threading Architecture",
                "expected_points": ["volatile ensures visibility across CPU caches and prevents reordering (happens-before), but NOT atomicity", "synchronized provides mutual exclusion (atomicity + visibility) via object monitor locks", "ReentrantLock offers advanced capabilities: fair locking, interruptible locks, tryLock with timeouts, condition variables"],
                "correct_answer": "volatile guarantees memory visibility across CPU caches and prevents instruction reordering via memory barriers, but does not provide atomic compound operations (like count++). synchronized enforces mutual exclusion, visibility, and atomicity via JVM monitor locks. ReentrantLock offers explicit locking with timeout support (tryLock), fairness policies, and multiple Condition queues.",
                "better_possible_answer": "\"volatile establishes a happens-before relationship ensuring immediate CPU cache flushing/invalidation, guaranteeing visibility without lock overhead, but does not guarantee atomicity for compound operations. `synchronized` provides mutual exclusion using intrinsic object monitors. `ReentrantLock` from java.util.concurrent provides explicit control: non-blocking `tryLock()`, interruptible lock acquisition, fairness guarantees, and Condition variables for fine-grained thread coordination.\""
            },
        ],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Dynamic Technical Question Generator for Custom / Manual Specializations
# ─────────────────────────────────────────────────────────────────────────────

def _generate_deterministic_hash(seed: str) -> str:
    return hashlib.md5(seed.encode("utf-8")).hexdigest()


def get_specialized_questions(
    specialization: str,
    round_num: int,
    language: str = "English",
    count: int = 6,
) -> List[QuestionItem]:
    """
    Returns a sequence of questions tailored to the specialization, round, and language.
    Guarantees:
    - Round 1 first question is ALWAYS Introduction.
    - Round 4 first question is ALWAYS Introduction (for comparative evaluation).
    - Round 4 last question is ALWAYS Closing Inquiry.
    - Questions match round difficulty and domain mechanics.
    """
    spec_clean = specialization.strip().lower()
    round_cfg = {1: "Easy", 2: "Moderate", 3: "Hard", 4: "Final"}.get(round_num, "Easy")
    questions: List[QuestionItem] = []

    # 1. Round 1 Opening: Intro
    if round_num == 1:
        questions.append(INTRO_QUESTION_ROUND1)

    # 2. Round 4 Opening: Intro
    if round_num == 4:
        questions.append(INTRO_QUESTION_ROUND4)

    # 3. Pull from Curated Bank if available
    curated_pool = []
    for known_key, rounds_dict in CURATED_QUESTIONS.items():
        if known_key in spec_clean or spec_clean in known_key:
            curated_pool = rounds_dict.get(round_cfg, [])
            break

    for q_data in curated_pool:
        questions.append(QuestionItem(
            id=q_data["id"],
            text_en=q_data["text_en"],
            text_hi=q_data.get("text_hi", q_data["text_en"]),
            text_hinglish=q_data.get("text_hinglish", q_data["text_en"]),
            difficulty=round_cfg,
            specialization=specialization,
            category=q_data.get("category", "Technical Competency"),
            expected_points=q_data.get("expected_points", []),
            correct_answer=q_data.get("correct_answer", ""),
            better_possible_answer=q_data.get("better_possible_answer", ""),
        ))

    # 4. If more questions are needed or for custom specializations, dynamically generate high-quality technical questions
    needed = count - len(questions) - (1 if round_num == 4 else 0)
    if needed > 0:
        dynamic_qs = _generate_dynamic_technical_questions(specialization, round_cfg, needed)
        questions.extend(dynamic_qs)

    # 5. Round 4 Closing question at end
    if round_num == 4:
        questions.append(CLOSING_QUESTION_ROUND4)

    return questions


def _generate_dynamic_technical_questions(specialization: str, difficulty: str, count: int) -> List[QuestionItem]:
    """Generates authentic domain-specific questions for any custom technical topic."""
    spec = specialization.strip()

    TEMPLATES = {
        "Easy": [
            {
                "topic": "Core Fundamentals & Paradigm",
                "en": f"What are the foundational principles and core architectural design patterns that define {spec}?",
                "hi": f"{spec} के मूलभूत सिद्धांत और मुख्य architectural design patterns क्या हैं?",
                "hinglish": f"{spec} ke fundamental principles aur core architectural design patterns kya hain aur yeh kab use hote hain?",
                "expected": [f"Core syntax and runtime environment of {spec}", "Fundamental problem domain solved", "Primary data types and execution model"],
                "correct": f"The core principles of {spec} involve its specific programming paradigms, memory allocation model, execution lifecycle, and standard library conventions.",
                "better": f"\"{spec} is structured around specific paradigms designed for [primary strength, e.g. performance/readability]. Its core architecture emphasizes clean separation of concerns, robust type systems, and deterministic execution.\"",
            },
            {
                "topic": "Data Handling & Memory Conventions",
                "en": f"How does data handling and memory lifecycle work in {spec}, and what common pitfalls should a developer avoid?",
                "hi": f"{spec} में डेटा हैंडलिंग और मेमोरी लाइफसाइकल कैसे काम करता है, और डेवलपर्स को किन गलतियों से बचना चाहिए?",
                "hinglish": f"{spec} mein data management aur memory lifecycle kaise operate karta hai, aur common pitfalls kya hote hain?",
                "expected": [f"Memory allocation and scope in {spec}", "Handling mutability and pass-by-reference/value", "Resource leaks and proper cleanup"],
                "correct": f"In {spec}, data is managed according to its variable scoping rules and memory management model. Common pitfalls include resource leakage, unintended mutations, and unhandled nil/null references.",
                "better": f"\"In {spec}, variables and state follow strict lifecycle rules. To write reliable code, developers must manage state mutability carefully, avoid holding unnecessary references in memory, and ensure explicit cleanup of I/O resources.\"",
            },
            {
                "topic": "Error Handling & Robustness",
                "en": f"How is error handling and exception safety structured in {spec} to build resilient applications?",
                "hi": f"{spec} में robust applications बनाने के लिए error handling और exception safety कैसे की जाती है?",
                "hinglish": f"{spec} mein robust applications build karne ke liye error handling aur exception handling best practices kya hain?",
                "expected": [f"Error propagation patterns in {spec}", "Distinguishing recoverable errors from fatal panics/crashes", "Safe recovery mechanisms"],
                "correct": f"Error handling in {spec} follows standard conventions (such as try/catch or explicit error returns). Resilient systems log contextual error details, clean up allocated handles, and fail gracefully.",
                "better": f"\"Robust error handling in {spec} requires categorizing errors into transient recoverable failures versus fatal invariant violations. We utilize structured error types, ensure teardown logic executes, and avoid swallowing errors silently.\"",
            },
        ],
        "Moderate": [
            {
                "topic": "Performance & Resource Optimization",
                "en": f"What profiling techniques, caching strategies, and code optimizations do you apply when scaling applications in {spec}?",
                "hi": f"{spec} में applications को स्केल करते समय आप कौन से profiling techniques और performance optimizations लागू करते हैं?",
                "hinglish": f"{spec} mein scaling ke dauran performance bottlenecks identify karne ke liye profiling aur optimization strategies kaise use karte hain?",
                "expected": [f"Benchmarking and CPU/memory profiling in {spec}", "Algorithmic complexity optimization", "I/O batching and connection pooling"],
                "correct": f"Optimizing {spec} applications involves identifying algorithmic bottlenecks (O(n^2) to O(n log n)), using built-in profiling tools, implementing connection pooling, and leveraging in-memory caching.",
                "better": f"\"When optimizing {spec}, I first profile CPU and heap usage to identify bottlenecks based on empirical data rather than guesswork. Common optimizations include reducing memory allocations, batching I/O requests, using concurrent pools, and caching hot query paths.\"",
            },
            {
                "topic": "Concurrency & Asynchronous Workflows",
                "en": f"How does concurrency, asynchronous processing, or thread management operate in {spec}, and how do you prevent race conditions?",
                "hi": f"{spec} में concurrency और asynchronous processing कैसे काम करती है, और आप race conditions को कैसे रोकते हैं?",
                "hinglish": f"{spec} mein concurrency aur async execution kaise manage hoti hai, aur thread safety ya race conditions ko kaise avoid karte hain?",
                "expected": [f"Concurrency primitives in {spec} (threads, async/await, coroutines/goroutines)", "Synchronization locks, atomics, or channels", "Deadlock avoidance"],
                "correct": f"Concurrency in {spec} is achieved via threading, event loops, or worker pools. Race conditions are prevented using mutexes, atomic operations, immutable message passing, or thread-safe queues.",
                "better": f"\"Concurrency in {spec} relies on [threads / coroutines / async loops]. To prevent race conditions, I adhere to immutable data sharing, employ fine-grained mutexes or channels, and avoid shared mutable state wherever possible.\"",
            },
        ],
        "Hard": [
            {
                "topic": "Architectural Trade-offs & Distributed State",
                "en": f"When architecting high-throughput production systems with {spec}, what trade-offs do you evaluate between latency, consistency, and fault tolerance?",
                "hi": f"{spec} के साथ high-throughput production systems बनाते समय आप latency, consistency और fault tolerance के बीच क्या trade-offs देखते हैं?",
                "hinglish": f"{spec} ke sath high-throughput production systems architect karte waqt latency, consistency aur fault tolerance ke trade-offs ko kaise balance karte hain?",
                "expected": [f"CAP theorem considerations in {spec} ecosystems", "Eventual consistency vs strong consistency", "Circuit breakers, retries, and backpressure"],
                "correct": f"Architecting production systems in {spec} involves trade-offs between sync/async architectures, replication lag, backpressure handling, and graceful degradation using circuit breakers.",
                "better": f"\"In high-scale {spec} architectures, I balance latency and consistency by choosing eventual consistency for non-critical paths while enforcing strict transactional boundaries for financial/core operations. I implement circuit breakers, exponential backoff with jitter, and dead-letter queues to maintain resilience under load.\"",
            },
        ],
        "Final": [
            {
                "topic": "Complex System Design & Edge-Case Forensics",
                "en": f"Describe a complex architectural failure, race condition, or memory leak in {spec} that you would diagnose and resolve in a mission-critical environment.",
                "hi": f"{spec} में किसी गंभीर production failure, memory leak या race condition का विश्लेषण आप root cause analysis के साथ कैसे करेंगे?",
                "hinglish": f"{spec} mein mission-critical production issue (jaise memory leak ya distributed deadlock) ko diagnose aur resolve karne ke liye aapka systematic approach kya hoga?",
                "expected": [f"Systematic root cause analysis methodology in {spec}", "Heap dump inspection, thread dump analysis, and metrics telemetry", "Safe zero-downtime rollback and architectural hardening"],
                "correct": f"Diagnosing critical issues in {spec} requires analyzing distributed traces, examining heap and thread dumps, isolating reproducing conditions in staging, patching the underlying root cause, and adding automated regression tests.",
                "better": f"\"My diagnostic framework begins with telemetry: isolating error spike timestamps, inspecting memory dumps, and reviewing distributed trace spans. Once identified, I implement a targeted hotfix with defensive boundary checks, verify under simulated load, deploy via canary rollout, and document a post-mortem with preventative monitoring alerts.\"",
            },
        ],
    }

    selected_templates = TEMPLATES.get(difficulty, TEMPLATES["Easy"])
    generated: List[QuestionItem] = []

    for i in range(count):
        tmpl = selected_templates[i % len(selected_templates)]
        q_id = f"dyn_{_generate_deterministic_hash(spec + difficulty + str(i))[:8]}_{i}"
        generated.append(QuestionItem(
            id=q_id,
            text_en=tmpl["en"],
            text_hi=tmpl["hi"],
            text_hinglish=tmpl["hinglish"],
            difficulty=difficulty,
            specialization=specialization,
            category=tmpl["topic"],
            expected_points=tmpl["expected"],
            correct_answer=tmpl["correct"],
            better_possible_answer=tmpl["better"],
        ))

    return generated
