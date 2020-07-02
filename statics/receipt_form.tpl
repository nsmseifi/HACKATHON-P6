<h1>Receipt FORM </h1>
    <script type="text/javascript">
    console.log("hello from msd");
        function addnewrow(){
        var table = document.getElementById("items");
        let total_rows = table.rows.length - 1; // subtract cause of header row
        var row = table.insertRow(1);
  let cell_prd = row.insertCell(0);
  let cell_qty = row.insertCell(1);
  let cell_price=row.insertCell(2);

  cell_prd.innerHTML = `<input type="text" required name="prd_${total_rows}" placeholder="Procuct"/>`;
  cell_qty.innerHTML = `<input type="number" required name="qty_${total_rows}" placeholder="Quantity"/>`;
  cell_price.innerHTML = `<input type="number" required name="price_${total_rows}" placeholder="Price"/>`;

        }
    </script>
<form method="post" action="add-new-receipt">
      <div class="container">

    <label for="title"><b>Title</b></label>
    <input type="text" placeholder="Receipt Title - optional" name="title" >

    <label for="payer"><b>Customer Name</b></label>
    <input type="text" placeholder="Customer Name" name="payer" >

      </div>
    <a onclick="addnewrow()">Add New Row</a>
<table id="items" style="margin: auto; width: 80%;">
    <thead>
    <tr>
        <th>Prd/Srv Title</th>
        <th>Qty</th>
        <th>Price</th>
    </tr>
    </thead>
    <tbody>
    </tbody>

</table>
    <div class="container">

    <label for="subtotal"><b>SubTotal Amount<sup>*</sup></b></label>
    <input type="number" placeholder="Receipt SubTotal Amount" name="subtotal" required >

    <label for="hst"><b>Total HST<sup>*</sup></b></label>
    <input type="number" placeholder="Receipt Total HST" name="hst" required >

    <label for="total_amount"><b>Total Amount<sup>*</sup></b></label>
    <input type="number" placeholder="Receipt Total Amount" name="total_amount" required >

    </div>
     <div class="clearfix">
      <button type="button" class="cancelbtn">Cancel</button>
      <button type="submit" class="signupbtn">Submit</button>
    </div>
</form>


    %rebase store_logged_in_layout
