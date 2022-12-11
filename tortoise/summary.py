import cohere
from PIL import Image
import pytesseract
import sys

co = cohere.Client(api_key)
min_text_threshold = 250 # characters
max_text_threshold = 430 # characters

'''
Primary Functions here:

summarize_pdf(filename): extracts text from given file and returns a summary, broken into sections
summarize(text): provides a summary for each section of the text (as a list of summaries)

'''

def summarize_image(filename):
    text = scan_file(filename)
    summaries = summarize(text)
    return '\n\n'.join(summaries)

def scan_file(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

def extract_sections(text:str, ub, lb):
    sections = text.split('\n\n')
    output = []
    for section in sections:
        for div in range(len(section) // 250):
            output.append(section[div*250:min(len(section),(div+1)*250)])
    return [output[:2]]

def summarize(text):
    global summary_prompt

    sections = extract_sections(text, max_text_threshold, min_text_threshold)
    summaries = []
    n_generations = 2

    for section in sections:
        summary_prompt += f'"{section}"\nIn Summary:"'

        response = co.generate( 
            model='xlarge', 
            prompt = summary_prompt,
            max_tokens=48, 
            temperature=0.5,
            stop_sequences=['"'],
            num_generations=n_generations,
            return_likelihoods = 'GENERATION',
            k=0,
            p=0.75,
        )

        gens = []
        likelihoods = []
        for gen in response.generations:
            gens.append(gen.text)
            sum_likelihood = 0
            for t in gen.token_likelihoods:
                sum_likelihood += t.likelihood
            # Get sum of likelihoods
            likelihoods.append(sum_likelihood)

        ix = likelihoods.index(min(likelihoods))
        summaries.append(gens[ix])
    return summaries

summary_prompt = '''
"A graph G0 = (V0
, E0
) is a subgraph of G = (V, E) if V0 ✓ V and E0 ✓ E.
A proper subgraph of G is any subgraph other than G itself.
A walk in an undirected graph G is a sequence of vertices, where each
adjacent pair of vertices are adjacent in G; informally, we can also think of a
walk as a sequence of edges. A walk is called a path if it visits each vertex
at most once. For any two vertices u and v in a graph G, we say that v is
reachable from u if G contains a walk (and therefore a path) between u and v.
An undirected graph is connected if every vertex is reachable from every other
vertex. Every undirected graph consists of one or more components, which are
its maximal connected subgraphs; two vertices are in the same component if
and only if there is a path between them."
In Summary: "A subgraph is a subset of the vertices and edges of a graph. A proper subgraph is a subgraph that is not the same as the original graph. A walk is a sequence of vertices in a graph and a path is a walk that only visits each vertex once. A graph is connected if every vertex is reachable from every other vertex. Every graph consists of one or more components, which are its maximal connected subgraphs."
"There are several dierent ways to represent these neighbor lists, but the
standard implementation uses a simple singly-linked list. The resulting data
structure allows us to list the (out-)neighbors of a node v in O(1 + deg(v)) time;
just scan v’s neighbor list. Similarly, we can determine whether uv is an edge
in O(1 + deg(u)) time by scanning the neighbor list of u. For undirected graphs,
we can improve the time to O(1 + min{deg(u), deg(v)}) by simultaneously
scanning the neighbor lists of both u and v, stopping either when we locate the
edge or when we fall of the end of a list.
a b c d e f g h i
b
e
a
e
c
g
l
j
k
a b c d
e f g
h i
j
m
l
k
Figure 5.9. An adjacency list for our example graph."
In Summary: "Adjacency lists are a way to represent a graph where each node has a list of neighbors. The list is typically implemented as a simple singly-linked list and allows us to list the (out-)neighbors of a node v in O(1 + deg(v)) time by scanning v’s neighbor list. We can also determine whether an edge exists between two nodes in O(1 + min{deg(u), deg(v)}) time by scanning the neighbor lists of both nodes."
"Comparison
Table . summarizes the performance of the various standard graph data
structures. Stars⇤ indicate expected amortized time bounds for maintaining
dynamic hash tables.
Standard adjacency list Fast adjacency list Adjacency
(linked lists) (hash tables) matrix
Space ⇥(V + E) ⇥(V + E) ⇥(V2)
Test if uv 2 E O(1 + min{deg(u), deg(v)}) = O(V) O(1) O(1)
Test if uv 2 E O(1 + deg(u)) = O(V) O(1) O(1)
List v’s (out-)neighbors ⇥(1 + deg(v)) = O(V) ⇥(1 + deg(v)) = O(V) ⇥(V)
List all edges ⇥(V + E) ⇥(V + E) ⇥(V2)
Insert edge uv O(1) O(1)
⇤ O(1)
Delete edge uv O(deg(u) + deg(v)) = O(V) O(1)
⇤ O(1)
In Summary: "Standard adjacency lists with linked lists have time bounds of O(1 + min{deg(u), deg(v)}) for testing if an edge is present and O(1 + deg(v)) for listing a node's neighbors. Adjacency lists with hash tables have a time bound of O(1) for these operations. Adjacency matrices have a time bound of O(1) for these operations but use more space. Adjacency lists with linked lists are still used because they are often good enough for most applications and avoid overhead."
"I claim that WFS marks every node reachable from s
and nothing else. The algorithm clearly marks each vertex in G at most once. To
show that it visits every node in a connected graph at least once, we modify the
algorithm slightly; the modifications are in bold red. Instead of keeping vertices
in the bag, the modified algorithm stores pairs of vertices. This modification
allows us to remember, whenever we visit a vertex v for the first time, which
previously-visited neighbor vertex put v into the bag. We call this earlier vertex
the parent of v."
In Summary: "The modified WFS algorithm claims to mark every node that is reachable from s and nothing else. This is because the algorithm visits each vertex in the graph at most once. The algorithm is modified slightly by storing pairs of vertices, allowing it to remember which vertex previously put v into the bag, and calling this earlier vertex the parent of v."
"The killer whale or orca (Orcinus orca) is a toothed whale
belonging to the oceanic dolphin family, of which it is the largest member"
In summary: "The killer whale or orca is the largest type of dolphin"
"It is recognizable by its black-and-white patterned body"
In Summary: "The killer whale or orca is the largest type of dolphin, known for its black-and-white patterned body."
'''

if __name__ == "__main__":
    # get the filename from the command line argument
    filename = sys.argv[1]

    summary = summarize_image(filename)

    print(summary)
