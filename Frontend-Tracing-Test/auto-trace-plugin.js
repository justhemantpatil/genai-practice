export default function autoTracePlugin({ types: t }) {
    return {
        name: 'auto-trace',
        visitor: {
            Program: {
                enter(path, state) {
                    state.hasDatatraced = false;
                },
                exit(path, state) {
                    if (state.hasDatatraced) {
                        let hasImport = false;
                        path.node.body.forEach(node => {
                            if (node.type === 'ImportDeclaration' && node.source.value === '/src/utils/tracer.js') {
                                hasImport = true;
                            }
                        });

                        if (!hasImport) {
                            const importDecl = t.importDeclaration(
                                [t.importSpecifier(t.identifier('trace'), t.identifier('trace'))],
                                t.stringLiteral('/src/utils/tracer.js')
                            );
                            path.node.body.unshift(importDecl);
                        }
                    }
                }
            },
            // 1. Handle Arrow Functions & Function Expressions: const foo = () => {}
            VariableDeclarator(path, state) {
                const { node } = path;
                if (!node.init) return;
                if (!['ArrowFunctionExpression', 'FunctionExpression'].includes(node.init.type)) return;

                const varName = node.id.name;
                if (!shouldTrace(varName)) return;
                if (isAlreadyTraced(node.init, t)) return;

                const { filename, basename, componentName } = getFileMeta(state);
                if (shouldSkipFile(filename)) return;

                const originalFn = node.init;
                node.init = createTraceCall(t, originalFn, varName, basename, componentName);
                state.hasDatatraced = true;
            },

            // 2. Handle Default Export Functions: export default function Dashboard() {}
            ExportDefaultDeclaration(path, state) {
                const decl = path.node.declaration;
                if (!t.isFunctionDeclaration(decl) || !decl.id) return;

                const funcName = decl.id.name;
                if (!shouldTrace(funcName)) return;
                if (isAlreadyTraced(decl, t)) return;

                const { filename, basename, componentName } = getFileMeta(state);
                if (shouldSkipFile(filename)) return;

                // Transform to: const Name = trace(function Name() {...}, ...); export default Name;
                const functionExpression = t.functionExpression(
                    decl.id,
                    decl.params,
                    decl.body,
                    decl.generator,
                    decl.async
                );

                const traceCall = createTraceCall(t, functionExpression, funcName, basename, componentName);
                const varDecl = t.variableDeclaration('const', [
                    t.variableDeclarator(decl.id, traceCall)
                ]);

                path.replaceWithMultiple([
                    varDecl,
                    t.exportDefaultDeclaration(decl.id)
                ]);

                state.hasDatatraced = true;
            },

            // 3. Handle Standard/Named Function Declarations: function App() {} or export function Foo() {}
            FunctionDeclaration(path, state) {
                // Skip if is child of ExportDefault (handled above)
                if (t.isExportDefaultDeclaration(path.parent)) return;

                const { node } = path;
                const funcName = node.id ? node.id.name : null;

                if (!funcName || !shouldTrace(funcName)) return;
                if (isAlreadyTraced(node, t)) return;

                const { filename, basename, componentName } = getFileMeta(state);
                if (shouldSkipFile(filename)) return;

                const functionExpression = t.functionExpression(
                    node.id,
                    node.params,
                    node.body,
                    node.generator,
                    node.async
                );

                const traceCall = createTraceCall(t, functionExpression, funcName, basename, componentName);
                const varDecl = t.variableDeclaration('const', [
                    t.variableDeclarator(node.id, traceCall)
                ]);

                // Safely replace based on context
                if (t.isExportNamedDeclaration(path.parent)) {
                    // Parent is 'export function Foo...', replace parent with 'export const Foo = ...'
                    // But replacing parent from here is dangerous? 
                    // Actually, replacing the child (FunctionDeclaration) with VariableDeclaration inside ExportNamedDeclaration IS valid AST.
                    // export const Foo = ... is ExportNamed(declaration: VariableDeclaration).
                    path.replaceWith(varDecl);
                } else {
                    path.replaceWith(varDecl);
                }

                state.hasDatatraced = true;
            }
        }
    };
}

function shouldTrace(name) {
    if (!name) return false;
    return name.startsWith('handle') || /^[A-Z]/.test(name);
}

function shouldSkipFile(filename) {
    return !filename || filename.includes('node_modules') || filename.includes('tracer.js');
}

function getFileMeta(state) {
    const filename = state.file.opts.filename || '';
    const basename = filename.split(/[\\/]/).pop();
    const componentName = basename.replace(/\.[^/.]+$/, "");
    return { filename, basename, componentName };
}

function createTraceCall(t, fnNode, fnName, fileName, componentName) {
    return t.callExpression(
        t.identifier('trace'),
        [
            fnNode,
            t.stringLiteral(fnName),
            t.stringLiteral(fileName),
            t.stringLiteral(componentName || 'Unknown')
        ]
    );
}

function isAlreadyTraced(node, t) {
    return t.isCallExpression(node) && t.isIdentifier(node.callee) && node.callee.name === 'trace';
}
