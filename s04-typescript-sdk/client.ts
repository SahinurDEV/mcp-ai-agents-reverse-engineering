// client.ts - a TypeScript MCP client: launch server.ts over stdio and use every primitive.
import { Client } from '@modelcontextprotocol/client';
import { StdioClientTransport } from '@modelcontextprotocol/client/stdio';

const client = new Client({ name: 's04-client', version: '1.0.0' });
await client.connect(new StdioClientTransport({ command: 'node', args: ['server.ts'] }));

const { tools } = await client.listTools();
console.log('tools:', tools.map(t => t.name));
const sum = await client.callTool({ name: 'add', arguments: { a: 2, b: 40 } });
console.log('add ->', sum.structuredContent);
const note = await client.readResource({ uri: 'notes://ghidra' });
const first = note.contents[0];
console.log('read ->', 'text' in first ? first.text : '(binary)');
const prompt = await client.getPrompt({ name: 'summarize_note', arguments: { name: 'mcp' } });
const msg = prompt.messages[0].content;
console.log('prompt ->', msg.type === 'text' ? msg.text : msg.type);
await client.close();
