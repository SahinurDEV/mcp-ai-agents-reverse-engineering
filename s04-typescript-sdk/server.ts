// server.ts - Section 4: the section 3 notes server, ported to the TypeScript SDK v2.
import { McpServer, ResourceTemplate } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import * as z from 'zod/v4';

const NOTES: Record<string, string> = {
  mcp: 'MCP connects hosts to servers over JSON-RPC.',
  ghidra: 'Ghidra is a free reverse engineering suite with a decompiler.',
};

const server = new McpServer({ name: 's04-ts-demo', version: '1.0.0' });

server.registerTool(
  'add',
  {
    description: 'Add two integers.',
    inputSchema: z.object({
      a: z.number().int().describe('First integer'),
      b: z.number().int().describe('Second integer'),
    }),
    outputSchema: z.object({ result: z.number().int() }),
  },
  async ({ a, b }) => {
    const output = { result: a + b };
    return { content: [{ type: 'text', text: String(output.result) }], structuredContent: output };
  },
);

server.registerResource(
  'index', 'notes://index',
  { description: 'List of all note names, one per line.', mimeType: 'text/plain' },
  async uri => ({ contents: [{ uri: uri.href, text: Object.keys(NOTES).sort().join('\n') }] }),
);

server.registerResource(
  'note', new ResourceTemplate('notes://{name}', {
    list: async () => ({ resources: Object.keys(NOTES).map(n => ({ uri: `notes://${n}`, name: n })) }),
  }),
  { description: 'Read one note by name.', mimeType: 'text/plain' },
  async (uri, variables) => {
    const name = String(variables.name);
    if (!(name in NOTES)) throw new Error(`no note named '${name}'; read notes://index for valid names`);
    return { contents: [{ uri: uri.href, text: NOTES[name] }] };
  },
);

server.registerPrompt(
  'summarize_note',
  {
    description: 'Ask the model to summarize a note in a given style.',
    argsSchema: z.object({ name: z.string(), style: z.string().optional() }),
  },
  ({ name, style }) => ({
    messages: [{ role: 'user', content: { type: 'text',
      text: `Summarize the note notes://${name} in ${style ?? 'one sentence'}. Quote the note before you summarize it.` } }],
  }),
);

await server.connect(new StdioServerTransport());
console.error('s04-ts-demo running on stdio');
