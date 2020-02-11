using System;
using Uml.Cs.Dll;

namespace Uml.Cs.App
{
    public static class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            var u = new UmlCsDll("Foo");
            u.IsValid();
        }
    }
}
