export default function uiTracePlugin({ types: t }) {
  return {
    visitor: {

      // 🔹 STEP 4A: Auto-inject import once per file
      Program(path, state) {
        const filename = state.file.opts.filename || "";
        
        // Skip uiLogger.js itself and node_modules
        if (filename.includes("uiLogger.js") || filename.includes("node_modules")) {
          return;
        }

        const hasImport = path.node.body.some(
          (node) =>
            node.type === "ImportDeclaration" &&
            node.source.value.includes("uiLogger")
        );

        if (!hasImport) {
          // Determine the correct relative path based on file location
          // Normalize the path to use forward slashes
          const normalizedPath = filename.replace(/\\/g, '/');
          
          // Find the src directory and calculate depth from there
          const srcIndex = normalizedPath.lastIndexOf('/src/');
          let importPath = "./utils/uiLogger";
          
          if (srcIndex !== -1) {
            // Get the part after /src/
            const afterSrc = normalizedPath.substring(srcIndex + 5); // +5 for '/src/'
            // Count directory levels (slashes)
            const dirDepth = (afterSrc.match(/\//g) || []).length;
            // Build the relative path
            importPath = (dirDepth > 0 ? '../'.repeat(dirDepth) : './') + "utils/uiLogger";
          }
          
          path.unshiftContainer(
            "body",
            t.importDeclaration(
              [
                t.importSpecifier(
                  t.identifier("sendUILog"),
                  t.identifier("sendUILog")
                )
              ],
              t.stringLiteral(importPath)
            )
          );
        }
      },

      // 🔹 STEP 4B: Only inject log into actual event handlers (onClick, onChange, onSubmit, etc)
      // Do NOT log render functions as they cause excessive logging
      CallExpression(path, state) {
        const filename = state.file.opts.filename || "";
        
        // Skip uiLogger.js itself and node_modules
        if (filename.includes("uiLogger.js") || filename.includes("node_modules")) {
          return;
        }

        // Only log specific event handlers
        const eventHandlers = [
          'handleLogin', 'handleLogout', 'handleClick', 'onChange',
          'onSubmit', 'onClick', 'onDelete', 'onAdd', 'onEdit',
          'handleSubmit', 'handleChange', 'handleDelete', 'handleAdd'
        ];

        // Check if this is a call to an event handler
        const calleeNode = path.node.callee;
        if (calleeNode.type === 'Identifier') {
          const functionName = calleeNode.name;
          
          // Only log if it matches our event handler names
          if (eventHandlers.some(handler => functionName.includes(handler))) {
            try {
              const logStatement = t.expressionStatement(
                t.callExpression(t.identifier("sendUILog"), [
                  t.objectExpression([
                    t.objectProperty(
                      t.identifier("type"),
                      t.stringLiteral("UI_EVENT")
                    ),
                    t.objectProperty(
                      t.identifier("event"),
                      t.stringLiteral(functionName)
                    ),
                    t.objectProperty(
                      t.identifier("file"),
                      t.stringLiteral(filename)
                    ),
                    t.objectProperty(
                      t.identifier("line"),
                      t.numericLiteral(path.node.loc?.start.line || 0)
                    )
                  ])
                ])
              );

              path.insertBefore(logStatement);
            } catch (e) {
              // Silently ignore errors in babel plugin
            }
          }
        }
      }
    }
  };
}
