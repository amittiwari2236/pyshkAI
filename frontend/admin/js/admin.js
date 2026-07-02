document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = '/api/cms/central-knowledge';
    let currentView = 'dashboard';
    let unifiedQuill = null;

    // Elements
    const contentArea = document.getElementById('content-area');
    const editorContainer = document.getElementById('editor-container');
    const pageTitle = document.getElementById('page-title');
    const saveBtn = document.getElementById('save-btn');
    const previewBtn = document.getElementById('preview-btn');
    const previewModal = document.getElementById('preview-modal');
    const previewContent = document.getElementById('preview-content');

    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.body.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            document.body.removeAttribute('data-theme');
            themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
        } else {
            document.body.setAttribute('data-theme', 'dark');
            themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
        }
    });

    // Initialize Quill Editor
    function initQuill() {
        if (!unifiedQuill) {
            unifiedQuill = new Quill('#quill-editor', {
                theme: 'snow',
                modules: {
                    toolbar: [
                        [{ 'header': [1, 2, 3, false] }],
                        ['bold', 'italic', 'underline', 'strike'],
                        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                        ['link', 'blockquote', 'code-block'],
                        ['clean']
                    ]
                },
                placeholder: 'Type or paste all the information for this module here...'
            });
        }
    }

    // Auth Headers (Using Django Session Auth)
    function getHeaders() {
        return {
            'Content-Type': 'application/json'
        };
    }

    async function fetchKnowledge(module) {
        try {
            const res = await fetch(`${API_BASE}/`, {
                headers: getHeaders()
            });
            if (res.status === 401 || res.status === 403) {
                alert('Session expired. Please log in again.');
                return { content: '' };
            }
            if (res.ok) {
                return await res.json();
            }
            return { content: '' };
        } catch (error) {
            console.error('Fetch error:', error);
            return { content: '' };
        }
    }

    async function saveKnowledge() {
        const content = unifiedQuill.root.innerHTML;
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';

        try {
            const res = await fetch(`${API_BASE}/`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({ content })
            });

            if (res.ok) {
                // Success styling
                saveBtn.innerHTML = '<i class="fa-solid fa-check"></i> Saved!';
                saveBtn.classList.remove('btn-primary');
                saveBtn.style.backgroundColor = '#10b981';
                setTimeout(() => {
                    saveBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Changes';
                    saveBtn.classList.add('btn-primary');
                    saveBtn.style.backgroundColor = '';
                    saveBtn.disabled = false;
                }, 2000);
            } else {
                alert('Failed to save content.');
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Changes';
            }
        } catch (error) {
            console.error('Save error:', error);
            alert('Error saving content.');
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Changes';
        }
    }

    saveBtn.addEventListener('click', saveKnowledge);

    // Preview
    previewBtn.addEventListener('click', () => {
        previewContent.innerHTML = unifiedQuill.root.innerHTML;
        previewModal.classList.remove('hidden');
    });

    document.querySelectorAll('#close-preview, #close-preview-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            previewModal.classList.add('hidden');
        });
    });

    // Sidebar navigation
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            document.querySelectorAll('.sidebar-nav a').forEach(a => a.classList.remove('active'));
            link.classList.add('active');
            
            currentView = link.getAttribute('data-view');
            pageTitle.textContent = link.textContent.trim();

            if (currentView === 'dashboard') {
                contentArea.classList.remove('hidden');
                editorContainer.classList.add('hidden');
                saveBtn.classList.add('hidden');
                previewBtn.classList.add('hidden');
                loadDashboard();
            } else {
                contentArea.classList.add('hidden');
                editorContainer.classList.remove('hidden');
                saveBtn.classList.remove('hidden');
                previewBtn.classList.remove('hidden');
                
                initQuill();
                unifiedQuill.root.innerHTML = '<p>Loading...</p>';
                unifiedQuill.disable();

                const data = await fetchKnowledge(currentView);
                
                unifiedQuill.enable();
                // Check if it's empty or just basic tags
                if (!data.content || data.content.trim() === '' || data.content === '<p><br></p>') {
                    unifiedQuill.root.innerHTML = '';
                } else {
                    unifiedQuill.root.innerHTML = data.content;
                }
            }
        });
    });

    // Dashboard loader
    async function loadDashboard() {
        contentArea.innerHTML = '<p>Loading analytics...</p>';
        try {
            const res = await fetch('/api/cms/dashboard/', { headers: getHeaders() });
            if(res.ok) {
                const data = await res.json();
                contentArea.innerHTML = `
                    <div class="stats-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                        <div class="stat-card" style="background: var(--glass-bg); padding: 20px; border-radius: 8px; border: 1px solid var(--glass-border);">
                            <h3>Unified Modules</h3>
                            <p style="font-size: 24px; font-weight: bold; color: var(--primary-color);">9</p>
                        </div>
                        <div class="stat-card" style="background: var(--glass-bg); padding: 20px; border-radius: 8px; border: 1px solid var(--glass-border);">
                            <h3>Status</h3>
                            <p style="font-size: 24px; font-weight: bold; color: #10b981;">Online</p>
                        </div>
                    </div>
                    <div style="margin-top: 30px; background: var(--glass-bg); padding: 20px; border-radius: 8px; border: 1px solid var(--glass-border);">
                        <h3>Welcome to the Unified Knowledge CMS</h3>
                        <p style="margin-top: 10px; color: var(--text-secondary);">
                            Select a module from the sidebar. You can paste all relevant information (e.g., all courses, or all teachers) into the rich text editor. The AI will intelligently search and extract exact answers from your provided text.
                        </p>
                    </div>
                `;
            } else {
                contentArea.innerHTML = '<p>Failed to load dashboard data.</p>';
            }
        } catch(e) {
            contentArea.innerHTML = '<p>Error loading dashboard.</p>';
        }
    }

    // Initial load
    loadDashboard();
});
