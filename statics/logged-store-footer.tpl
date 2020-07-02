		<footer id="footer">
            <div class="container">
                <div class="row double">
                    <div class="6u">
                        <div class="row collapse-at-2">
                            <div class="6u">
                                <h3>DREP</h3>
                                <ul class="alt">
                                    <li><a target="_blank" href="https://www.usatoday.com/story/money/2019/11/25/receipts-101-digital-receipts-grow-popularity-but-paper-still-king/4180900002/">Digital Receipts</a></li>
                                    <li><a target="_blank" href="https://www.who.int/">WHO</a></li>
                                </ul>
                            </div>
                            <div class="6u">
                                <h3>The Team</h3>
                                <ul class="alt">
                                    <li><a target="_blank" href="https://www.senecacollege.ca/home.html">Seneca</a></li>
                                    <li><a target="_blank" href="https://www.senecacollege.ca/school/software-design-and-data-science/seneca-hackathon.html">Hackathon</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="6u">
                        <h2>About Us</h2>
                        <p>DREP (Digital Receipts and Expense Payments) was created in solving the issue of paperless transactions. Covid-19 has impacted millions and to prevent furthur spread of fture viruses, our team developed a solution to limit hand to hand transmission.</p>
                        <ul class="icons">
                            <li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
                            <li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
                            <li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>
                            <li><a href="#" class="icon fa-linkedin"><span class="label">LinkedIn</span></a></li>
                            <li><a href="#" class="icon fa-pinterest"><span class="label">Pinterest</span></a></li>
                        </ul>
                    </div>
                </div>
                <ul class="copyright">
                    <li>&copy; VISNK. All rights reserved.</li>
                    <li>Design: <a href="http://templated.co">TEMPLATED</a></li>
                    <li>Images: <a href="http://unsplash.com">Unsplash</a></li>
                </ul>
            </div>
        </footer>

        <script type='text/javascript'>
            let receipt_data = [];
            const submitUserSignUp = (ev)=>{
                ev.preventDefault();  //to stop the form submitting
                var receipt_data = {
                    cell_no: document.getElementById('user-phone').value,
                    username: document.getElementById('user-username').value,
                    password: document.getElementById('user-password').value,
                    name: document.getElementById('user-name').value,
                    address: document.getElementById('user-address').value,
                    email: document.getElementById('user-email').value,
                };

                for (var i = 0; i < receipt_data.length ; i++) {
                    receipt_data.push(receipt_data[i]);

                }
                console.log(receipt_data)
                document.forms[0].reset(); // to clear the form for the next entries
                //document.querySelector('form').reset();

                //saving to localStorage
                localStorage.setItem('user_signup', JSON.stringify(receipt_data) );
            }

            receipt_data = [];
            const submitStoreSignUp = (ev)=>{
                ev.preventDefault();  //to stop the form submitting
                var receipt_data = {
                    phone: document.getElementById('store-phone').value,
                    store_name: document.getElementById('store-name').value,
                    store_email: document.getElementById('store-email').value,
                    store_password: document.getElementById('store-password').value,
                    store_address: document.getElementById('store-address').value,
                };
                console.log(receipt_data)
                for (var i = 0; i < receipt_data.length ; i++) {
                    receipt_data.push(receipt_data[i]);

                }
                document.forms[0].reset(); // to clear the form for the next entries
                //document.querySelector('form').reset();

                //saving to localStorage
                localStorage.setItem('store_signup', JSON.stringify(receipt_data) );
            }




            document.addEventListener('DOMContentLoaded', ()=>{
            document.getElementById('booton').addEventListener('click', submitUserSignUp);
            });


            document.addEventListener('DOMContentLoaded', ()=>{
            document.getElementById('booton_2').addEventListener('click', submitStoreSignUp);
            });

        </script>
