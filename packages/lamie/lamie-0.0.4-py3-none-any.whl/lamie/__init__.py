def p1():
    a = """
    using System;
    namespace COL
{
class COL
{
public COL()
{
Console.WriteLine("***********Constructor Overloading***********");
Console.WriteLine("One value for AOC");
Console.WriteLine("Two values for AOR");
Console.WriteLine("Three values for EB Bill");
Console.WriteLine("***********$$$$$$$$$$$$$$$$$$$$$$$***********");
}
public COL(double r)
{
Console.WriteLine("The Area of Circle for the radius value "+r+" is "+(3.14*r*r));
}
public COL(double w,double h)
{
Console.WriteLine("The Area of Rectangle is " + (w * h));
}
public COL(int pr, int cr,double ur)
{
int tr = cr - pr;
Console.WriteLine("The Bill Amount for the reading " +tr+" is "+ (tr*ur));
}
}
class Pgm2
{
static void Main(string[] args)
{
COL c1=new COL();
Console.WriteLine("Enter the radious value to calculate AOC ");
double r=Convert.ToDouble(Console.ReadLine());
COL c2=new COL(r);
Console.WriteLine("Enter the width and height to calculate AOR ");
double w=Convert.ToDouble(Console.ReadLine());
double h=Convert.ToDouble(Console.ReadLine());
COL c3 = new COL(w,h);
Console.WriteLine("Enter the Previous Reading, Current Reading and Unit price to
calculate EB Bill ");
int pr=Convert.ToInt32(Console.ReadLine());
int cr=Convert.ToInt32(Console.ReadLine());
double ur=Convert.ToDouble(Console.ReadLine());
COL c4=new COL(pr,cr,ur);
}
}
}
    """
    print(a)


def p2():
    b = """
    using System;
namespace MOCS
{
class MO
{
public void Find(int n)
{
int c = n;
int i;
int[] a = new int[10];
for (i = 0; n > 0; i++)
{
a[i] = n % 2;
n = n / 2;
}
Console.Write("Binary of the given number " + c + " is ");
for (i = i - 1; i >= 0; i--)
{
Console.Write(a[i]);
}
}
public void Find(int bs, double da, double ta, double hra, double ma)
{
double a1 = bs * da;
double a2 = bs * ta;
double a3 = bs * hra;
double a4 = bs * ma;
double ns=bs+a1+a2+a3+a4;
Console.WriteLine("Your Net Salary is "+ns);
}
}
class Pgm4
{
static void Main(string[] args)
{
MO obj=new MO();
Console.WriteLine("Enter the number to convert into binary:");
int a = Convert.ToInt32(Console.ReadLine());
obj.Find(a);
Console.WriteLine("\n Enter the basic salary:");
int bs = Convert.ToInt32(Console.ReadLine());
Console.WriteLine("Enter the DA allowance like 0.10 ");
double da = Convert.ToDouble(Console.ReadLine());
Console.WriteLine("Enter the TA allowance like 0.10 ");
double ta = Convert.ToDouble(Console.ReadLine());
Console.WriteLine("Enter the HRA allowance like 0.10 ");
double hra = Convert.ToDouble(Console.ReadLine());
Console.WriteLine("Enter the MA allowance like 0.10 ");
double wa = Convert.ToDouble(Console.ReadLine());
obj.Find(bs, da, ta, hra, wa);
}
}
}
    """
    print(b)


def p3():
    c = """
    using System;
namespace ConsoleApp5
{
 class FD
 {
 public int p, y;
 public double r, i;
 public virtual void calculate()
 { }
 }
 class SBI : FD
 {
 public SBI() { Console.WriteLine("Welcome to SBI: FD Scheme"); }
 public void get()
 {
 Console.WriteLine("\n Enter Principle Amount : ");
 p = Convert.ToInt32(Console.ReadLine());
 Console.WriteLine("\n Enter Number of Years to deposit : ");
 y = Convert.ToInt32(Console.ReadLine());
 }
 public override void calculate()
 {
 if (y >= 1 && y <= 2)
 {
 r = 6.8;
 Console.WriteLine("The Principle Amount: " + p);
 Console.WriteLine("Number of years: " + y);
 Console.WriteLine("The Interest Rate is: " + r);
 i = p * y * r / 100;
 Console.WriteLine("Interest you have earned is " + i);
 Console.WriteLine("Fixed Deposit amount is " + (i + p));
 }
 else if (y > 2 && y <= 5)
 {
 r = 7.8;
 Console.WriteLine("The Principle Amount: " + p);
 Console.WriteLine("Number of years: " + y);
 Console.WriteLine("The Interest Rate is: " + r);
 i = p * y * r / 100;
 Console.WriteLine("Interest you have earned is " + i);
 Console.WriteLine("Fixed Deposit amount is " + (i + p));
 }
 if (y > 5)
 {
 r = 8;
 Console.WriteLine("The Principle Amount: " + p);
 Console.WriteLine("Number of years: " + y);
 Console.WriteLine("The Interest Rate is: " + r);
 i = p * y * r / 100;
 Console.WriteLine("Interest you have earned is " + i);
 Console.WriteLine("Fixed Deposit amount is " + (i + p));
 }
 }
 }
 class UBI : FD
 {
 public UBI() { Console.WriteLine("Welcome to Union Bank of India: FD 
Scheme"); }
 public void get()
 {
 Console.WriteLine("\n Enter Principle Amount : ");
 p = Convert.ToInt32(Console.ReadLine());
 Console.WriteLine("\n Enter Number of Years to deposit : ");
 y = Convert.ToInt32(Console.ReadLine());
 }
 public override void calculate()
 {
 if (y >= 1 && y <= 2)
 {
 r = 6.3;
 Console.WriteLine("The Principle Amount: " + p);
 Console.WriteLine("Number of years: " + y);
 Console.WriteLine("The Interest Rate is: " + r);
 i = p * y * r / 100;
 Console.WriteLine("Interest you have earned is " + i);
 Console.WriteLine("Fixed Deposit amount is " + (i + p));
 }
 else if (y > 2 && y <= 5)
 {
 r = 6.8;
 Console.WriteLine("The Principle Amount: " + p);
 Console.WriteLine("Number of years: " + y);
 Console.WriteLine("The Interest Rate is: " + r);
 i = p * y * r / 100;
 Console.WriteLine("Interest you have earned is " + i);
 Console.WriteLine("Fixed Deposit amount is " + (i + p));
 }
 if (y > 5)
 {
 r = 7.3;
 Console.WriteLine("The Principle Amount: " + p);
 Console.WriteLine("Number of years: " + y);
 Console.WriteLine("The Interest Rate is: " + r);
 i = p * y * r / 100;
 Console.WriteLine("Interest you have earned is " + i);
 Console.WriteLine("Fixed Deposit amount is " + (i + p));
 }
 }
 }
 class FixedDeposit
 {
 public static void Main()
 {
 string bn;
 Console.WriteLine("Enter the Bank in which you want to make a FD:SBI OR 
UBI");
 bn = Console.ReadLine();
 if (bn.Equals("SBI"))
 {
 SBI sbi = new SBI();
 sbi.get();
 sbi.calculate();
 }
 else
 {
 UBI ubi = new UBI();
 ubi.get();
 ubi.calculate();
 }
 }
 }
}
    """
    print(c)


def p4():
    d = """
    using System;
namespace ConsoleApp3
{
 class Student
 {
 public int roll;
 public string name;
 public void getdata()
 {
 Console.WriteLine("\n____");
 Console.WriteLine("\n Enter Roll No.: ");
 roll = Convert.ToInt32(Console.ReadLine());
 Console.WriteLine("\n Enter Name: ");
 name = Console.ReadLine();
 }
 public void putdata()
 {
 Console.WriteLine("\n-----------------");
 Console.WriteLine("\n**Student Markslist**");
 Console.WriteLine("\n-----------------");
 Console.WriteLine("\n Roll Number: " +roll);
 Console.WriteLine("\n Student Name: "+name);
 }
 }
 class StudentExam : Student
 {
 public int hindi, english, kannada;
 public double per;
 public void accept_data()
 {
 getdata();
 Console.WriteLine("\n Enter Marks for Hindi: ");
 hindi=Convert.ToInt32(Console.ReadLine());
 Console.WriteLine("\n Enter Marks for English: ");
 english = Convert.ToInt32(Console.ReadLine());
 Console.WriteLine("\n Enter Marks for Kannada: ");
 kannada = Convert.ToInt32(Console.ReadLine());
 }
 public void display_data()
 {
 putdata();
 Console.WriteLine("\n Marks of Hindi: " +hindi);
 Console.WriteLine("\n Marks of English: "+ english);
 Console.WriteLine("\n Marks of Kannada: "+ kannada);
 }
 }
 class StudentResult:StudentExam
 {
 public void calculate()
 {
 double t = hindi + english + kannada;
 per = t / 6.0;
 Console.WriteLine("\n The total percentage: "+ per);
 Console.WriteLine("\n--------------------------");
 }
 }
 class Result
 {
 public static void Main(string[] args)
 {
 StudentResult str = new StudentResult();
 int cnt, i;
 Console.WriteLine("\n Enter the number of Students you want?: ");
 cnt = Convert.ToInt32(Console.ReadLine());
 for(i=0;i<cnt;i++)
 {
 str.accept_data();
 str.display_data();
 str.calculate();
 }
 }
 }
}
    """
    print(d)


def p5():
    e = """
    using System;
namespace CA10
{
public delegate void rectDelegate(double heights, double width);
class rectangle
{
public void area(double height,double width)
{
Console.WriteLine("Area is:{0}", (width * height));
}
public void perimeter(double height,double width)
{
Console.WriteLine("Perimeter is:{0}", 2 * (width + height));
}
}
class Pgm10
{
public static void Main(String[]args)
{
rectangle rect = new rectangle();
rectDelegate rectdele = new rectDelegate(rect.area);
rectdele += rect.perimeter;
rectdele.Invoke(6.3, 4.2);
Console.WriteLine();
rectdele.Invoke(16.3, 10.3); 
}
}
}
    """
    print(e)


def p6():
    f = """
    : <%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs" 
Inherits="ASPApplication.WebForm1" %>
<!DOCTYPE html>
<html>
<head runat="server">
 <title>Server Control</title>
</head>
<body>
 <form id="form1" runat="server">
 <h1>Ice & Chill</h1>
 <h3>Ice Cream Bill</h3>
 <asp:Label ID="l1" runat="server" Text="Menu"></asp:Label>
 <asp:ListBox ID="menu" runat="server" AutoPostBack="True" 
OnSelectedIndexChanged="menu_SelectedIndexChanged">
 <asp:ListItem Text="Mint Chocolate" Value="Mint Chocolate"/>
 <asp:ListItem Text="Butterscotch" Value="Butterscotch"/>
 <asp:ListItem Text="Strawberry" Value="Strawberry"/>
 <asp:ListItem Text="French Vanilla" Value="French Vanilla"/>
 <asp:ListItem Text="Caramel Ice" Value="Caramel Ice"/>
 <asp:ListItem Text="Blackcurrent" Value="Blackcurrent"/>
 </asp:ListBox><br/>
 <asp:Label ID="l2" runat="server" Text="Items"></asp:Label>
 <asp:ListBox ID="item" runat="server" AutoPostBack="True" 
OnSelectedIndexChanged="item_SelectedIndexChanged"></asp:ListBox><br />
 <asp:Label ID="l3" runat="server" Text="Quantity"></asp:Label>
 <asp:TextBox ID="txtquantity" runat="server" AutoPostBack="True" 
OnTextChanged="txtquantity_TextChanged"></asp:TextBox><br />
 <asp:Label ID="l4" runat="server" Text="Price"></asp:Label>
 <asp:TextBox ID="txtprice" runat="server"></asp:TextBox><br />
 <asp:Label ID="l5" runat="server" Text="Amount"></asp:Label>
 <asp:TextBox ID="txtamount" runat="server"></asp:TextBox><br />
 <asp:Label ID="l6" runat="server" Text="Grand Total"></asp:Label>
 <asp:TextBox ID="txtgrandtotal" runat="server" Text="0"></asp:TextBox><br />
 </form>
</body>
</html>
Server Page:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Globalization;
using System.Text;
using System.Threading;
namespace ASPApplication
{
 public partial class WebForm1 : System.Web.UI.Page
 {
 protected void menu_SelectedIndexChanged(object sender, EventArgs e)
 {
 item.Items.Add(menu.Text);
 }
 protected void item_SelectedIndexChanged(object sender, EventArgs e)
 {
 txtquantity.Text = " ";
 txtprice.Text = " ";
 txtamount.Text = " ";
 if (item.Text == "Mint Chocolate")
 {
 txtprice.Text = "119";
 }
 else if (item.Text == "Butterscotch")
 {
 txtprice.Text = "89";
 }
 else if (item.Text == "Strawberry")
 {
 txtprice.Text = "99";
 }
 else if (item.Text == "French Vanilla")
 {
 txtprice.Text = "149";
 }
 else if (item.Text == "Caramel Ice")
 {
 txtprice.Text = "59";
 }
 else if (item.Text == "Blackcurrent")
 {
 txtprice.Text = "79";
 }
 }
 protected void txtquantity_TextChanged(object sender, EventArgs e)
 {
 double price = Convert.ToDouble(txtprice.Text);
 double quantity = Convert.ToDouble(txtquantity.Text);
 double grandtotal = Convert.ToDouble(txtgrandtotal.Text);
 txtamount.Text =(price * quantity).ToString();
 double amount = Convert.ToDouble(txtamount.Text);
 txtgrandtotal.Text = (grandtotal + amount).ToString();
 }
 }
}
    """
    print(f)


def p7():
    g = """
    <%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Client1.aspx.cs" 
Inherits="ASPAppplication1.Client1" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title>ASP APP I</title>
 <meta charset="utf-8"/>
 <meta name="viewport" content="width=device-width, initial-scale=1"/>
 <link rel="stylesheet" 
href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css"/>
 <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.4/dist/jquery.slim.min.js"></script>
 <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
 <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>
 <link rel="stylesheet" href="StyleSheet1.css" />
</head>
<body>
 <form id="form1" runat="server">
 <div class="container col-sm-6 text-center">
 <br /><br />
 <h1 class="text-center">STUDENT DATABASE</h1>
 <br /><br /><br />
 <div>
 <asp:Label ID="Label1" runat="server">NAME : </asp:Label>
 <asp:TextBox ID="TextBox1" runat="server" class="form-control"></asp:TextBox>
 <asp:RequiredFieldValidator ID="RequiredFieldValidator3" runat="server"
 ErrorMessage="Mandatory Field" ControlToValidate="TextBox1" Display = "Dynamic">
 </asp:RequiredFieldValidator>
 <asp:RegularExpressionValidator ID="RegularExpressionValidator1" runat="server"
 ErrorMessage="Enter only characters" ControlToValidate="TextBox1"
 ValidationExpression="^[a-zA-Z ]*$" Display = "Dynamic">
 </asp:RegularExpressionValidator>
 </div>
 <div>
 <asp:Label runat="server" ID="Label2">AGE : </asp:Label>
 <asp:TextBox runat="server" ID="TextBox2" class="form-control"></asp:TextBox>
 <asp:RangeValidator ID="RangeValidator1" runat="server"
 ErrorMessage="Enter age between 18 to 35" ControlToValidate="TextBox2" 
MaximumValue="35" MinimumValue="18" Type="Integer" Display = "Dynamic"></asp:RangeValidator>
 </div>
 <div>
 <asp:Label ID="Label3" runat="server">PASSWORD : </asp:Label>
 <asp:TextBox ID="TextBox3" runat="server" class="form-control"></asp:TextBox>
 <asp:RequiredFieldValidator ID="RequiredFieldValidator2" runat="server"
 ErrorMessage="Mandatory Field" ControlToValidate="TextBox3" Display = "Dynamic">
 </asp:RequiredFieldValidator>
 </div>
 
 <div>
 <asp:Label ID="Label4" runat="server">RETYPE PASSWORD : </asp:Label>
 <asp:TextBox ID="TextBox4" runat="server" class="form-control"></asp:TextBox>
 <asp:RequiredFieldValidator ID="RequiredFieldValidator4" runat="server"
 ErrorMessage="Mandatory Field" ControlToValidate="TextBox4" Display = "Dynamic">
 </asp:RequiredFieldValidator>
 <asp:CompareValidator ID="CompareValidator1" runat="server" ControlToCompare="TextBox3"
 ControlToValidate="TextBox4" Display="Dynamic" ErrorMessage="Password does not match"
 Operator="Equal">
 </asp:CompareValidator>
 </div>
 
 <div>
 <asp:Label ID="Label5" runat="server">ADDRESS : </asp:Label>
 <asp:TextBox ID="TextBox5" runat="server" class="form-control" ></asp:TextBox>
 <asp:RequiredFieldValidator ID="RequiredFieldValidator5" runat="server"
 ErrorMessage="Mandatory Field" ControlToValidate="TextBox5" Display = "Dynamic">
 </asp:RequiredFieldValidator>
 </div>
 
 <div>
 <asp:Label ID="Label6" runat="server">PHONE NUMBER : </asp:Label>
 <asp:TextBox ID="TextBox6" runat="server" class="form-control"></asp:TextBox>
 <asp:RequiredFieldValidator ID="RequiredFieldValidator6" runat="server"
 ErrorMessage="Mandatory Field" ControlToValidate="TextBox6" Display = "Dynamic">
 </asp:RequiredFieldValidator>
 <asp:RegularExpressionValidator ID="RegularExpressionValidator4" runat="server" 
ControlToValidate="TextBox6"
 ErrorMessage="Phone number should be 10 digits" ValidationExpression="[0-9]{10}" Display = 
"Dynamic">
 </asp:RegularExpressionValidator>
 </div>
 
 <div>
 <asp:Label ID="Label7" runat="server">EMAIL : </asp:Label>
 <asp:TextBox ID="TextBox7" runat="server" class="form-control"></asp:TextBox>
 <asp:RequiredFieldValidator ID="RequiredFieldValidator7" runat="server"
 ErrorMessage="Mandatory Field" ControlToValidate="TextBox7" Display = "Dynamic">
 </asp:RequiredFieldValidator>
 
 <asp:Button ID="btnsubmit" runat="server" Text="SUBMIT" OnClick="btnsubmit_Click"/>
 <br />
 <asp:Label ID="lblmsg" runat="server" class="text-center"></asp:Label>
 </div>
 </form>
</body>
</html>
SERVER PAGE :
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace ASPAppplication1
{
 public partial class Client1 : System.Web.UI.Page
 {
 protected void btnsubmit_Click(object sender, EventArgs e)
 {
 lblmsg.Text = "Validation Successful";
 }
 }
}
    """
    print(g)



