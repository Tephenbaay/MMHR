<!-- Profile Section -->
            <div class="relative">
                <button id="profile-btn" class="flex items-center space-x-2 py-2 px-4 bg-green-500 rounded-full hover:bg-green-600">
                    <img src="/static/uploads/profile-avatar.png" alt="Profile" class="h-8 w-8 rounded-full">
                    <span class="hidden md:block">John Doe</span>
                </button>

                <!-- Profile Dropdown -->
                <div id="profile-menu" class="hidden absolute right-0 mt-2 bg-white text-black w-48 rounded-lg shadow-lg">
                    <a href="#" class="block px-4 py-2 hover:bg-gray-100">View Profile</a>
                    <a href="#" class="block px-4 py-2 hover:bg-gray-100">Settings</a>
                    <a href="#" class="block px-4 py-2 hover:bg-gray-100">Logout</a>
                </div>
            </div>

            <script>
        // Profile Dropdown Toggle
        document.getElementById('profile-btn').addEventListener('click', () => {
            const menu = document.getElementById('profile-menu');
            menu.classList.toggle('hidden');
        });
    </script>
